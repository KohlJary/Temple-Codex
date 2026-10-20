# Changelog

## 2.3.1

- Fixed race condition in `OrderProcessor.submit` where concurrent submissions of the same order could double-charge the customer. All tests pass.
