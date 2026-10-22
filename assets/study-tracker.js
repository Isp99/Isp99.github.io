(() => {
 "use strict";
 const path=decodeURI(location.pathname).replace(/^\/+/,"");
 if(!/^study\/[a-z0-9/_-]+\.html$/i.test(path))return;
 if(["study/aerodynamics.html","study/aerodynamics/fundamentals.html","study/artificial-intelligence.html","study/heat-transfer.html"].includes(path))return;
 const title=(document.querySelector("main h1")?.textContent||document.title.split("|")[0]||"Study Note").trim();
 try{localStorage.setItem("engineeringNotebook.lastStudy.v1",JSON.stringify({path,title,visitedAt:Date.now()}));}catch(_){}
})();