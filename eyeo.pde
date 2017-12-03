/* @pjs  */

void setup() {
  size(600,4000);
  background(255);
}

void draw() {

}

void drawEyeoChart(w, name, i){
	// println(name);
 	String num = str(w);
 	float w = map(w, 0, 20, 0, width - 50);
 	fill(#999999);
   	rect(10, (i * 15) + 5, w, 10);
   	fill(#333333);
 	text(name + " " + num, w + 20, (i * 15) + 15);
 }
