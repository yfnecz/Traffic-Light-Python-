# Traffic-Light-Python-

This is the educational project in Python about the Traffic Management System.

The program has three possible states:
- Not Started — the state until the initial settings have been provided;
- Menu — the state that shows possible options and processes the user's input;
- System — the state that shows the user information about the traffic light, such as time from startup and the number of roads, etc.

The program first welcomes the user and prompts them to input the number of roads and the interval between the opening and closing of each road. Then the control panel with menu is displayed.

When the user provided input for initial settings (both the number of roads and the interval), a new thread QueueThread is created to implement the System state, this newly-created thread performs these actions each second:
- Increases the variable that corresponds to the amount of time since the "system startup" each second (1000 milliseconds);
- (if in System state) Prints the system information.

By choosing 3 option in Menu, the program switches to the System state, and the main thread waits for input from the user. To return to the Menu state, the user should press Enter.

Let's consider a scenario where we want to control 4 roads, with an interval of 8 seconds. We add all the roads sequentially via the "1. Add" option: "First", "Second", "Third", "Fourth". After all the roads are added and the interval has been specified, we can start our system with "3. System":
```
! 11s. have passed since system startup !
! Number of roads: 4 !
! Interval: 8 !

Road "First" will be open for 8s.
Road "Second" will be closed for 8s.
Road "Third" will be closed for 16s.
Road "Fourth" will be closed for 24s.

! Press "Enter" to open menu !
```

The roads are "connected" in a circular queue, where the road at the front of the queue is open, and the rest are closed. In this case, "First" was added first, so it is also the first to be open. It will remain open for the specified interval of 8 seconds before switching to the next road in line. So, "Second" will open after "First" in 8 seconds, "Third" will open after "Second" in 16 seconds, and "Fourth" will open after "Third" in 24 seconds.

For example, if the remaining time for "First" is 1 second, the system will display:
```
Road "First" will be open for 1s.
Road "Second" will be closed for 1s.
Road "Third" will be closed for 9s.
Road "Fourth" will be closed for 17s.
```
Once the timer for the open road expires, it moves to the back of the queue, and the next road becomes open:
```
Road "First" will be closed for 24s.
Road "Second" will be open for 8s.
Road "Third" will be closed for 8s.
Road "Fourth" will be closed for 16s.
```


If the opened road is deleted, there will be no roads in state open until the next one opens.

If the only road that exists is the opened one - it will never close (its state will always stay open), but still will count down the time to close.

When there are no roads in the system, the next added road will be open for an interval.



Example of execution:

<img src="https://github.com/user-attachments/assets/0ffea8bf-57a6-4c0d-9168-0036ecd204c6" width="600">

Example of input data:

<img src="https://github.com/user-attachments/assets/866ff73c-4d08-47ff-b7d6-ee26b2cce3ba" width="600">



