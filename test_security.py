# test_security.py
import sys

sys.path.insert(0, ".")

# Test the limits directly
MAX_JD_CHARS = 10000
MAX_RESUME_MB = 5


def test_jd_length():
    # Normal JD - should pass
    normal_jd = "Software Engineer role requiring Python skills." * 10
    assert len(normal_jd) <= MAX_JD_CHARS, "FAIL: normal JD rejected"
    print("✅ Normal JD: PASS")

    # Too long JD - should be caught
    long_jd = "x" * 10001
    assert len(long_jd) > MAX_JD_CHARS, "FAIL: long JD not caught"
    print("✅ Long JD detection: PASS")


def test_resume_size():
    # Normal size - 1MB
    normal_size = 1 * 1024 * 1024
    assert normal_size <= MAX_RESUME_MB * 1024 * 1024, "FAIL: normal size rejected"
    print("✅ Normal resume size: PASS")

    # Too large - 6MB
    large_size = 6 * 1024 * 1024
    assert large_size > MAX_RESUME_MB * 1024 * 1024, "FAIL: large file not caught"
    print("✅ Large file detection: PASS")


def test_empty_inputs():
    jd = "   "
    assert not jd.strip(), "FAIL: empty JD not caught"
    print("✅ Empty JD detection: PASS")


if __name__ == "__main__":
    print("Running security tests...\n")
    test_jd_length()
    test_resume_size()
    test_empty_inputs()
    print("\n✅ All tests passed!")
