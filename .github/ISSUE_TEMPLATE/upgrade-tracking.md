---
name: Python/Kivy Version Upgrade Tracking
about: Track compatibility testing and upgrades for Python, Kivy, Cython, or NDK versions
title: "Upgrade: [Component] from [current] to [target]"
labels: ["enhancement", "ci", "dependencies"]
assignees: []
---

## Upgrade Summary

**Component:** [e.g., Python, Kivy, Cython, python-for-android]  
**Current Version:** [e.g., 3.10.13]  
**Target Version:** [e.g., 3.12.0]  
**Priority:** [Low / Medium / High]  
**Estimated Effort:** [Low: 1-2 days | Medium: 3-5 days | High: 1+ weeks]

## Motivation

- [ ] Security update
- [ ] Bug fix
- [ ] End-of-life (deprecation)
- [ ] Feature access
- [ ] Performance improvement
- [ ] Other: _______________

## Technical Assessment

### Compatibility Concerns
- [ ] C-extension API changes (CPython, Cython)
- [ ] Dependency version conflicts
- [ ] Platform/architecture support
- [ ] Device compatibility (API levels)
- [ ] Build toolchain compatibility

### Risk Level
- [ ] Low (known compatible; patch version bump)
- [ ] Medium (minor version change; limited testing needed)
- [ ] High (major version; significant testing required)

## Test Plan

### Phase 1: Build Verification
- [ ] Create feature branch: `test/[component]-[version]`
- [ ] Update `buildozer.spec` with new version
- [ ] Trigger CI build for both arm64-v8a and armeabi-v7a
- [ ] Capture build logs
- [ ] **Result:** [Pass ✓ | Fail ✗ | Partial ⚠]
- [ ] Build log artifact: [link or paste relevant errors]

### Phase 2: APK Validation
- [ ] APK file generated successfully
- [ ] APK size is reasonable (within ±10% of baseline)
- [ ] APK signature valid
- [ ] Install test on emulator/device
- [ ] App launches without crash
- [ ] **Result:** [Pass ✓ | Fail ✗]

### Phase 3: Functional Testing
- [ ] Main UI loads and renders correctly
- [ ] WiFi list retrieval works
- [ ] Network connectivity (login, API calls)
- [ ] Profile switching functionality
- [ ] Settings access
- [ ] No visual regressions
- [ ] Performance acceptable (startup time, memory usage)
- [ ] **Result:** [Pass ✓ | Fail ✗ | Minor Issues ⚠]

### Phase 4: Device Matrix Testing (if applicable)
- [ ] Test on API 24 (armeabi-v7a)
- [ ] Test on API 33 (arm64-v8a)
- [ ] Test on physical device if available
- [ ] **Result:** [Pass ✓ | Fail ✗]

## Blockers & Issues Found

### Build Issues
```
[Paste compiler errors or logs here]
```

### Runtime Issues
```
[Paste crash logs or functional test failures here]
```

### Known Workarounds
- [ ] Workaround 1: _______________
- [ ] Workaround 2: _______________

## Implementation Plan

### Files to Update
- [ ] `buildozer.spec` — Version pinning
- [ ] `.github/workflows/build.yml` — If toolchain changes needed
- [ ] `docs/UPGRADE_ROADMAP.md` — Update compatibility matrix
- [ ] `scripts/ci_smoke_test.sh` — If test requirements change

### Checklist Before Merge
- [ ] All tests pass (CI + device)
- [ ] No regressions in core functionality
- [ ] Build logs reviewed for warnings
- [ ] Commit messages clear and linked to this issue
- [ ] PR review completed
- [ ] Changelog updated (if applicable)

## Rollback Plan

If deployment fails:
1. Revert commit: `git revert <commit-hash>`
2. Restore previous build artifacts if needed
3. Document root cause and blockers

**Rollback commit:** [to be filled if needed]

## References

- **Roadmap:** [docs/UPGRADE_ROADMAP.md](../../docs/UPGRADE_ROADMAP.md)
- **CI Hardening:** [docs/scripts/README.md](../../scripts/README.md)
- **Upstream Release Notes:** [link]
- **Related Issues:** [link other issues]

## Acceptance Criteria

- [ ] CI build passes for both architectures with no C-extension errors
- [ ] APK installs and app launches successfully
- [ ] All functional tests pass without regression
- [ ] Device testing completed on target API levels
- [ ] PR reviewed and approved
- [ ] Merged to main and stable release cut (if applicable)

---

**Created:** [Date]  
**Last Updated:** [Date]  
**Owner:** @[assignee]
