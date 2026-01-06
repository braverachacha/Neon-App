/* NAVBAR TOGGLE & MOBILE */
const sidebar = document.getElementById("sidebar") || null;
const toggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if(toggle && sidebar){
  toggle.addEventListener("click",(e)=>{
    e.stopPropagation();
    sidebar.classList.toggle("active");
    toggle.classList.toggle("active");
  });
}

if(toggle && navLinks){
  toggle.addEventListener("click",(e)=>{
    e.stopPropagation();
    navLinks.classList.toggle("active");
    toggle.classList.toggle("active");
  });
}

window.addEventListener("click",(e)=>{
  if(navLinks && !navLinks.contains(e.target) && !toggle.contains(e.target)){
    navLinks.classList.remove("active");
    toggle.classList.remove("active");
  }
  if(sidebar && !sidebar.contains(e.target) && !toggle.contains(e.target)){
    sidebar.classList.remove("active");
    toggle.classList.remove("active");
  }
});

if(navLinks){
  navLinks.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", ()=>{
      navLinks.classList.remove("active");
      toggle.classList.remove("active");
    });
  });
}

/* PARTICLES BACKGROUND */
const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");
let particles = [];
const COUNT = 80;
function resize(){ canvas.width=window.innerWidth; canvas.height=window.innerHeight;}
window.addEventListener("resize",resize);
resize();

class Particle{
  constructor(){
    this.x=Math.random()*canvas.width;
    this.y=Math.random()*canvas.height;
    this.size=Math.random()*2+1;
    this.vx=(Math.random()-0.5)*0.6;
    this.vy=(Math.random()-0.5)*0.6;
  }
  update(){ this.x+=this.vx; this.y+=this.vy;
    if(this.x<0||this.x>canvas.width)this.vx*=-1;
    if(this.y<0||this.y>canvas.height)this.vy*=-1;
  }
  draw(){
    ctx.beginPath();
    ctx.arc(this.x,this.y,this.size,0,Math.PI*2);
    ctx.fillStyle="rgba(0,255,247,0.8)";
    ctx.shadowBlur=10;
    ctx.shadowColor="#00fff7";
    ctx.fill();
  }
}

function init(){ particles=[]; for(let i=0;i<COUNT;i++){particles.push(new Particle());}}
function animate(){ ctx.clearRect(0,0,canvas.width,canvas.height); particles.forEach(p=>{p.update(); p.draw();}); requestAnimationFrame(animate);}
init(); animate();

