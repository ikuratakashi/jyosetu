import React from 'react';
import { useGamepad } from '../utils/useGamepad';

function GameComponent() {

  let 
    left = false, 
    up = false, 
    right = false, 
    down = false, 
    buttonA = false, 
    buttonB = false, 
    buttonX = false, 
    buttonY = false, 
    LB = false, 
    LT = false, 
    RB = false, 
    RT = false, 
    start = false, 
    select = false,
    joystickBtn = false,
    joystickRightBtn = false;
  let joystick = [0, 0], joystickRight = [0, 0];

  try {
    const gamepadState = useGamepad();
    if (!gamepadState) {
      throw new Error("No gamepad connected");
    }

    left = gamepadState.left ?? false;
    up = gamepadState.up ?? false;
    right = gamepadState.right ?? false;
    down = gamepadState.down ?? false;
    buttonA = gamepadState.buttonA ?? false;
    buttonB = gamepadState.buttonB ?? false;
    buttonX = gamepadState.buttonX ?? false;
    buttonY = gamepadState.buttonY ?? false;
    LB = gamepadState.LB ?? false;
    LT = gamepadState.LT ?? false;
    RB = gamepadState.RB ?? false;
    RT = gamepadState.RT ?? false;
    start = gamepadState.start ?? false;
    select = gamepadState.select ?? false;
    joystick = gamepadState.joystick ?? [0, 0];
    joystickRight = gamepadState.joystickRight ?? [0, 0];
    joystickBtn = gamepadState.joystickBtn ?? false;
    joystickRightBtn = gamepadState.joystickRightBtn ?? false;
    select = gamepadState.select ?? false;
  } catch (error) {
    console.error("Error using gamepad:", error);
    return <div>No gamepad connected</div>;
  }

  return (
    <div>
      <div>{left ? 'Button left Pressed' : 'Press Button left'}</div>
      <div>{up ? 'Button up Pressed' : 'Press Button up'}</div>
      <div>{right ? 'Button right Pressed' : 'Press Button right'}</div>
      <div>{down ? 'Button down Pressed' : 'Press Button down'}</div>
      <div>{buttonA ? 'Button A Pressed' : 'Press Button A'}</div>
      <div>{buttonB ? 'Button B Pressed' : 'Press Button B'}</div>
      <div>{buttonX ? 'Button X Pressed' : 'Press Button X'}</div>
      <div>{buttonY ? 'Button Y Pressed' : 'Press Button Y'}</div>
      <div>{LB ? 'Button LB Pressed' : 'Press Button LB'}</div>
      <div>{LT ? 'Button LT Pressed' : 'Press Button LT'}</div>
      <div>{RB ? 'Button RB Pressed' : 'Press Button RB'}</div>
      <div>{RT ? 'Button RT Pressed' : 'Press Button RT'}</div>
      <div>{start ? 'Button start Pressed' : 'Press Button start'}</div>
      <div>{select ? 'Button select Pressed' : 'Press Button select'}</div>
      <div>{joystickBtn ? 'Button joystickBtn Pressed' : 'Press joystickBtn select'}</div>
      <div>{joystickRightBtn ? 'Button joystickRightBtn Pressed' : 'Press Button joystickRightBtn'}</div>
      <div>Joystick L: 
        <div>{joystick[0]}</div>
        <div>{joystick[1]}</div>
      </div>
      <div>Joystick R: 
        <div>{joystickRight[0]}</div>
        <div>{joystickRight[1]}</div>
      </div>
    </div>
  );
}

export default GameComponent;
