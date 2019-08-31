// Imports
import p5 from 'p5/lib/p5.min' //loads the correct minified 388KB file!

const copter = {
  y: 50
}

p5.keyPressed() {

}

p5.setup() {
  createCanvas(500, 500);
}

p5.draw() {

  ellipse(250, 250, 50, copter.y)
}

document.addEventListener('keyup', keyPressed)