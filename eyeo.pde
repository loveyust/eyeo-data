/* @pjs  */

float[] myNumbers = {22, 10, 15, 26, 30, 35, 32};

void setup() {
  size(600,4000);
  background(200);
}

void draw() {
  drawBarChart(myNumbers);
}

void drawBarChart(float data[]){
  //println(data);
/* for (int i = 0; i < data.length; i++) {
    float w = map(data[i], 0, max(data), 0, width - 50);
    rect(10, (i * 25) + 5, w, 20);
    text(data[i], w + 20, (i * 25) + 20 );
   }*/
 }

 void drawEyeoChart(w, name, i){
  println(name);
  String num = str(w);
 	 float w = map(w, 0, 20, 0, width - 50);
   rect(10, (i * 15) + 5, w, 10);
 	text(name + " " + num, w + 20, (i * 15) + 15);
   
 }

Point addPoint(int x, int y) {
	Point pt = new Point(x,y);
	points.add(pt);
	return pt;
}

class Point {
	int x,y;
	Point(int x, int y) { this.x=x; this.y=y; }
	void draw() {
		stroke(255,0,0);
		fill(255);
		ellipse(x,y,10,10);
	}
}
