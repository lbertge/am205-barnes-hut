// A class to describe a group of Particles
// An ArrayList is used to manage the list of Particles
import java.util.Scanner;
class ParticleSystem {
  ArrayList<Particle> particles;
  PVector origin;

  ParticleSystem(PVector position) {
    origin = position.copy();
    particles = new ArrayList<Particle>();
  }

  void addParticle() {
    particles.add(new Particle(origin));
  }
  void addParticle(float x, float y){
     particles.add(new Particle(new PVector(x, y))); 
  }

  void run() {
    for (int i = particles.size()-1; i >= 0; i--) {
      Particle p = particles.get(i);
      p.run();
      if (p.isDead()) {
        particles.remove(i);
      }
    }
  }
}

// A simple Particle class

class Particle {
  PVector position;
  PVector velocity;
  PVector acceleration;
  float lifespan;

  Particle(PVector l) {
    acceleration = new PVector(0, 0.05);
    velocity = new PVector(random(-1, 1), random(-2, 0));
    position = l.copy();
    lifespan = 255.0;
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    //velocity.add(acceleration);
    //position.add(velocity);
    lifespan -= 5.0;
  }

  // Method to display
  void display() {
    stroke(255, lifespan);
    fill(255, lifespan);
    ellipse(position.x, position.y, 2, 2);
  }

  // Is the particle still useful?
  boolean isDead() {
    if (lifespan < 0.0) {
      return true;
    } else {
      return false;
    }
  }
}

void readFile() {
  String [] lines = loadStrings("result-00-00.csv");
  for (String line : lines) {
    System.out.println(line);
  }
}



ParticleSystem ps;
String[] lines;
int index = 0;

void setup() {
  readFile();
  size(1000, 1000);
  ps = new ParticleSystem(new PVector(width/2, 50));
  ps.addParticle();
  lines = loadStrings("result2.csv");
  frameRate(100000);
  fill(255);
  stroke(255);
   smooth(8);
  noStroke();
}

void draw() {
  background(0);
     String[] pieces = split(lines[index % lines.length],  ",");
     for(int i = 0; i < pieces.length; i+=2){
    
       float x = 400 + float(pieces[i]) / 1e11;
       float y = 200 + float(pieces[i+1]) / 1e11;
       
       ps.addParticle(x,y);
     }
  index+=3;
  ps.run();
}
