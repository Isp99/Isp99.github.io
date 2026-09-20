'use strict';
document.addEventListener('DOMContentLoaded',()=>{
 const links=[...document.querySelectorAll('.right-sidebar a[href^="#"]')];
 const headings=links.map(a=>document.getElementById(a.hash.slice(1))).filter(Boolean);
 const update=()=>{let current=headings[0];for(const h of headings)if(h.getBoundingClientRect().top<=150)current=h;
   if(!current)return;for(const a of links){const active=a.hash==='#'+current.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');}};
 let pending=false;window.addEventListener('scroll',()=>{if(pending)return;pending=true;requestAnimationFrame(()=>{update();pending=false;});},{passive:true});update();
 const current=document.querySelector('.left-sidebar .sidebar-link.active');const container=document.querySelector('.left-sidebar .sidebar-inner');
 if(current&&container&&container.scrollHeight>container.clientHeight)container.scrollTop=Math.max(0,current.offsetTop-container.clientHeight/3);
});
