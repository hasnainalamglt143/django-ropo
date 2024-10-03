document.addEventListener("DOMContentLoaded", () => {
    const next = document.querySelector("button#next");
    const prev = document.querySelector("button#previous");
    const post_container = document.querySelector(".posts");
    const page_info = document.querySelector("span.page_info");

    // Fetch and display the first page on initial load
    // fetchPage(1);

    next.addEventListener("click", (e) => {
        let current = parseInt(e.target.dataset.id);
        let maxPage = parseInt(page_info.innerHTML.match(/of\s+(\d+)/)[1]);

        if (current + 1 <= maxPage) {
            fetchPage(current + 1);
        }
    });

    prev.addEventListener("click", (e) => {
        let current = parseInt(e.target.dataset.id);
        console.log(current)

        if (current -1>0) {
            

            fetchPage(current - 1);
        } 
    });

    function fetchPage(page) {
    fetch(`page/${page}/`, {
         
            method: "GET",
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');

            }
            return response.json();
        })
        .then(data => {
            post_container.innerHTML = populate(data); // Populate posts
            navigate(data); // Update navigation controls
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    }

    function populate(data) {
        return data.posts.map(post => `
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-9/12 mx-auto mt-10 h-auto">
                <div class="flex items-center mb-4">
                    <img class="w-12 h-12 rounded-full mr-4" src="${post.profile_pic}" alt="Profile Picture">
                    <div>
                        <h4>${post.author}</h4>
                        <p class="text-gray-600">${post.created_at}</p>
                    </div>
                </div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">${post.title}</h3>
                <p class="mb-4 h-fit ">${post.content}.</p>
            </div>`).join("");
    }

    function navigate(data) {
        prev.dataset.id = data.current_page;
        next.dataset.id = data.current_page;
        page_info.innerHTML = `page ${data.current_page} of ${data.page_num}`;

        // Disable buttons if no previous/next page
        prev.disabled = !data.has_previous;
        next.disabled = !data.has_next;
    }




//menue bar for responsiveness
const menue_icon=document.getElementById("menu-bar")
const menue=document.getElementById("menu")
console.log(menue,menue_icon)
menue_icon.addEventListener("click",()=>{
    menue.classList.toggle("hidden")

})


})
