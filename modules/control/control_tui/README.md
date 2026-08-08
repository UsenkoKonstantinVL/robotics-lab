# Control TUI

This C++ application publishes `ControlCommand` samples on
`robotics_lab.control.command` at 10 Hz.

- Up publishes the selected positive maximum.
- Down publishes the selected negative maximum.
- Left and Right decrease or increase the maximum in steps of `0.1`.
- A publish cycle without a new Up or Down event sends zero.
- `q` exits and publishes a final zero command.

Build the project, then run the app in an interactive terminal:

```bash
dev/dev.sh exec build/dev/modules/control/control_tui/robotics_lab_control_tui
```
