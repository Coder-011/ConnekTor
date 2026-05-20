# ConnekTor Python/Kivy/NDK Upgrade Roadmap

**Current State (as of May 2026):**
- Python: 3.10.13 (pinned for Kivy 2.3.0 compatibility)
- Kivy: 2.3.0
- Cython: 0.29.32
- Android NDK: r28c
- Min API: 21 | Target API: 33

**Objective:** Safely upgrade to newer Python versions (3.12+, targeting 3.14) while maintaining build reproducibility and app functionality.

---

## Phase 1: Documentation & Assessment (Current)

### Deliverables
- [ ] This roadmap document ✓
- [ ] Compatibility matrix (Python 3.10 → 3.14)
- [ ] Known issues and workarounds tracker
- [ ] Local test procedure documentation

### Compatibility Matrix

| Component | Current | Target | Status | Notes |
|-----------|---------|--------|--------|-------|
| Python | 3.10.13 | 3.14.0 | ❌ Not tested | CPython C-API changes likely; requires validation |
| Kivy | 2.3.0 | 2.4+ | ⚠️ Check upstream | Kivy 2.3.0 wheels may not support Python 3.12+ |
| Cython | 0.29.32 | 0.30+ | ⚠️ Check | Cython version must match generated wrappers in Kivy |
| Android NDK | r28c | r28c (stable) | ✓ OK | NDK r28c supports Python 3.14 targets |
| Min API | 21 | 24+ (recommended) | ⚠️ Plan | Consider minimum API 24 for better native support |

### Risk Assessment

**High Risk:**
- Kivy 2.3.0 C extensions may not compile with Python 3.12+ due to CPython C-API breaking changes
- `_PyObject_*` macros removed in Python 3.11+; Cython-generated code from older Kivy may not work
- Older Kivy wheels may not be available for newer Python versions

**Medium Risk:**
- python-for-android may need newer version to support Python 3.12+
- Build times may increase due to fewer cached artifacts for newer Python
- Device compatibility (older Android versions may have issues with newer stdlib)

**Low Risk:**
- App code changes (our Python is compatible across 3.10-3.14)
- Dependencies (requests, certifi, etc. support Python 3.12+)

---

## Phase 2: Python 3.10 → 3.11 Testing (Fallback Safety Check)

**Objective:** Validate 3.11 as an intermediate stepping stone; confirm Kivy 2.3.0 support.

### Procedure

1. **Create feature branch:** `test/python-3.11`
2. **Update buildozer.spec:**
   ```
   requirements = python3==3.11.9,kivy==2.3.0,...
   ```
3. **Run CI build:**
   - Monitor logs for `_Py*` symbol errors or Cython mismatches
   - If build succeeds → APK smoke test on emulator
   - If build fails → Compare errors with 3.10; document blockers

4. **Local device test (if CI passes):**
   - Install APK on physical device/emulator
   - Test core flows:
     - App launch (no crash)
     - WiFi list retrieval
     - Login flow (network calls)
     - Profile switching
   - Document any behavioral changes

5. **Decision point:**
   - ✓ All tests pass → Proceed to Phase 3
   - ✗ Tests fail → Analyze root cause; may require Kivy patch or p4a upgrade
   - ⚠️ Partial failures → Document as known issues; consider CI workaround

### Success Criteria

- [ ] CI build completes with no C-extension errors
- [ ] APK installs on both arm64-v8a and armeabi-v7a
- [ ] App launches and main screen renders
- [ ] WiFi scanning and login flows work without crashes
- [ ] Performance is acceptable (no obvious slowdowns vs. 3.10)

---

## Phase 3: Python 3.12 Testing (Targeted Upgrade)

**Objective:** Validate 3.12 compatibility; identify if Kivy 2.3.0 requires patching or if we need Kivy 2.4+.

### High-Level Steps

1. **Create branch:** `test/python-3.12`
2. **Update requirements:**
   ```
   requirements = python3==3.12.0,kivy==2.3.0,...
   ```
3. **Attempt CI build:**
   - Expected: C-extension compile errors due to CPython C-API changes
   - Capture full error logs for analysis

4. **If build fails (likely scenario):**
   - Check if Kivy 2.4+ has been released with Python 3.12 support
   - Evaluate options:
     - **Option A:** Upgrade to Kivy 2.4+ (requires testing KivyMD compatibility)
     - **Option B:** Wait for Kivy 2.3.1+ patch (upstream depends on timing)
     - **Option C:** Fork & patch Kivy 2.3.0 (high maintenance cost, not recommended)

5. **If Option A (Kivy upgrade):**
   - Create separate branch: `test/kivy-2.4`
   - Update: `requirements = python3==3.12.0,kivy==2.4.0,...`
   - Pin Cython to version compatible with Kivy 2.4 wrappers
   - Repeat build + device tests
   - Check KivyMD compatibility (may require minor UI code changes)

6. **Device QA (if build succeeds):**
   - Same test matrix as Phase 2
   - Plus: UI regression testing (ensure KivyMD widgets work correctly)

### Decision Matrix

| Scenario | Action | Branch | Owner |
|----------|--------|--------|-------|
| Python 3.12 + Kivy 2.3.0 → Success | Merge to main; promote to stable | `test/python-3.12` | Release Manager |
| Python 3.12 + Kivy 2.3.0 → Compile fail | Try Kivy 2.4+ | `test/kivy-2.4` | Core Dev |
| Python 3.12 + Kivy 2.4+ → Success | QA and merge | `test/kivy-2.4` | Core Dev + QA |
| Python 3.12 + Kivy 2.4+ → Failure | Document as blocker; stay on 3.11 | N/A | Tech Lead |

---

## Phase 4: Python 3.13–3.14 Stretch Goals

**Objective:** Plan future upgrades beyond 3.12; document long-term strategy.

### Timeline Estimate

- **Python 3.13** (Oct 2024): Feasible after 3.12 stabilization
- **Python 3.14** (Oct 2025): Target for 2026+ releases

### Acceptance Criteria (for any new Python version)

- [ ] CI pipeline completes cleanly for both ARM architectures
- [ ] No C-extension or C-API compatibility errors
- [ ] APK size is within 5% of current build
- [ ] Smoke tests pass on Android API 24–33 devices
- [ ] Core app flows tested on real devices or cloud testing service
- [ ] No regressions in WiFi scanning, login, or profile management
- [ ] Build time is reasonable (~15 min baseline)

---

## Implementation Guidelines

### For Each Test Phase:

1. **Pre-test checklist:**
   - Ensure CI pipelines have stable storage (no surprise cache evictions)
   - Tag a baseline commit on main for rollback
   - Set up device/emulator testing infrastructure

2. **Testing scope:**
   - Automated: CI build, APK integrity checks, basic launch test
   - Manual: Device-based QA of core workflows (WiFi, login, navigation)
   - Performance: Compare APK size, startup time vs. current baseline

3. **Failure handling:**
   - Document exact error message and stack trace
   - Check Kivy/p4a/Cython upstream issues for known problems
   - If blocker: update this roadmap with the issue and defer to later phase

4. **Success criteria:**
   - Merge branch into a staging/pre-release branch
   - Run extended QA (24+ hours of stability testing if possible)
   - Create GitHub release with changelog
   - Announce to users/developers via release notes

---

## Long-term Maintenance Strategy

### Quarterly Reviews
- Monitor upstream releases: Python, Kivy, Cython, p4a, Android NDK
- Assess deprecation timelines (e.g., Python 3.10 EOL: Oct 2026)
- Plan upgrades 1–2 quarters ahead to avoid pressure

### Pinning Policy
- Pin all language runtime versions (Python, Cython, p4a)
- Review pin versions before each major release
- Maintain a compatibility matrix in this document

### Deprecated Version Handling
- Plan to drop support for Python 3.10 by end of 2026
- Migrate to Python 3.12 as minimum by late 2025
- Archive build artifacts for old versions for emergency rollback

---

## Related Issues & PRs

- **PR #XX (hotfix):** Pin Python 3.10.13 (CI stability)
- **PR #YY (hardening):** Add build caching, debug logging, smoke tests
- **Issue #ZZ (future):** Track Kivy 2.4+ compatibility work (to be created)

---

## Questions & Support

For questions about this roadmap:
1. Check this document for common scenarios
2. Ask in GitHub Discussions or create an issue
3. Review CI logs from test branches for detailed error messages

**Last Updated:** May 2026  
**Maintainer:** ConnekTor Core Team
