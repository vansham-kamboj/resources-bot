const form = document.getElementById("research-form");
const webCol = document.getElementById("web-resources");
const videoCol = document.getElementById("video-resources");

form.addEventListener("submit", async e => {
    e.preventDefault();
    const query = document.getElementById("query").value.trim();
    if(!query) return;

    webCol.innerHTML = "<p>⏳ Searching web resources...</p>";
    videoCol.innerHTML = "<p>⏳ Searching videos...</p>";

    const formData = new FormData();
    formData.append("query", query);

    try {
        const res = await fetch("/research", {method:"POST", body:formData});
        const data = await res.json();

        webCol.innerHTML = "";
        videoCol.innerHTML = "";

        if(data.resources.length === 0){
            webCol.innerHTML = "<p>No resources found.</p>";
            videoCol.innerHTML = "<p>No videos found.</p>";
            return;
        }

        data.resources.forEach(r => {
            const div = document.createElement("div");
            div.className = "resource";
            div.innerHTML = `<a href="${r.link}" target="_blank">${r.title}</a><p>${r.snippet}</p>`;

            if(r.link.includes("youtube.com/watch")){
                videoCol.appendChild(div);
            } else {
                webCol.appendChild(div);
            }
        });
    } catch(err){
        console.error(err);
        webCol.innerHTML = "<p>❌ Error fetching resources.</p>";
        videoCol.innerHTML = "<p>❌ Error fetching videos.</p>";
    }
});
