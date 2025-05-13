% Initial state description for Shakey's world
% Rooms, corridors, doors, light switches, and boxes
initial_state([
    % Room setup
    at(shakey, room3),       % Shakey starts in room3
    connected(room1, corridor), connected(corridor, room1),
    connected(room2, corridor), connected(corridor, room2),
    connected(room3, corridor), connected(corridor, room3),
    connected(room4, corridor), connected(corridor, room4),
    
    % Light states - initially all on
    lightOn(room1), lightOn(room2), lightOn(room3), lightOn(room4),
    
    % Box positions
    box(box1), box(box2),
    at(box1, room1), at(box2, room3),
    on(box1, floor), on(box2, floor),
    on(shakey, floor),
    
    % Light switch locations
    lightSwitch(switch1, room1),
    lightSwitch(switch2, room2),
    lightSwitch(switch3, room3),
    lightSwitch(switch4, room4)
]).

% Goal state 1: Move Shakey from room3 to room1
goal_state1([at(shakey, room1)]).

% Goal state 2: Switch off the light in room1
goal_state2([lightOff(room1)]).

% Goal state 3: Get box2 into room2
goal_state3([at(box2, room2)]).

% STRIPS Actions

% Action: go(X, Y) - Move from location X to location Y
act(go(X, Y), 
    % Preconditions
    [at(shakey, X), connected(X, Y)], 
    % Delete list
    [at(shakey, X)], 
    % Add list
    [at(shakey, Y)]).

% Action: push(B, X, Y) - Push box B from location X to location Y
act(push(B, X, Y),
    % Preconditions
    [at(shakey, X), at(B, X), box(B), lightOn(X), on(B, floor), on(shakey, floor), connected(X, Y)],
    % Delete list
    [at(shakey, X), at(B, X)],
    % Add list
    [at(shakey, Y), at(B, Y)]).

% Action: climbUp(B) - Climb onto box B
act(climbUp(B),
    % Preconditions
    [at(shakey, X), at(B, X), box(B), on(B, floor), on(shakey, floor)],
    % Delete list
    [on(shakey, floor)],
    % Add list
    [on(shakey, B)]).

% Action: climbDown(B) - Climb down from box B
act(climbDown(B),
    % Preconditions
    [on(shakey, B), box(B)],
    % Delete list
    [on(shakey, B)],
    % Add list
    [on(shakey, floor)]).

% Action: turnOn(S) - Turn light switch S on
act(turnOn(S),
    % Preconditions
    [lightSwitch(S, R), at(shakey, R), on(shakey, B), box(B), at(B, R), lightOff(R)],
    % Delete list
    [lightOff(R)],
    % Add list
    [lightOn(R)]).

% Action: turnOff(S) - Turn light switch S off
act(turnOff(S),
    % Preconditions
    [lightSwitch(S, R), at(shakey, R), on(shakey, B), box(B), at(B, R), lightOn(R)],
    % Delete list
    [lightOn(R)],
    % Add list
    [lightOff(R)]).