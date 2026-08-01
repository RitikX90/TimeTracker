const url = "http://127.0.0.1:8000"
const ul = document.getElementById("history-list")
const start_button = document.getElementById("start-btn")
const subject = document.getElementById("subject");
const notes = document.getElementById("notes");
const current_session = document.getElementById("current-session")
const active_session_div = document.getElementById("active-session")
const no_active_session_div = document.getElementById("no-active-session")


export async function delete_session(id, li){
    try{
        const response = await fetch(`${url}/api/delete/${id}`,{
            method:"DELETE",
        });
        if(response.ok){
            console.log("Session Deleted")
            li.remove()
        }
    }catch(error){
        console.error(`Network Error ${error}`)
    }
}

export function show_timer(difference){

    // console.log(difference)
    const hours = Math.floor((difference % (1000*60*60*24)) / (1000*60*60))
    const minutes = Math.floor((difference % (1000*60*60)) / (1000*60))
    const seconds = Math.floor((difference % (1000*60)) / (1000))
    const paddedHours = String(hours).padStart(2, '0');
    const paddedMinutes = String(minutes).padStart(2, '0');
    const paddedSeconds = String(seconds).padStart(2, '0');
    return `${paddedHours}:${paddedMinutes}:${paddedSeconds}`;
}

export function render_history(sessions){
    sessions.forEach(session => {
        const card = document.createElement('li')
        card.classList.add("history-card")
        card.innerHTML = `
        <div class="history-details">
        <h3>${session.id}</h3>
        <h3>${session.subject}</h3>
        <p>Duration: ${show_timer(session.duration * 1000)}</p>
        </div>
        <button class="delete-btn">Delete</button>
        `;
        const delete_button = card.querySelector(".delete-btn")
        delete_button.addEventListener("click", () => delete_session(session.id, card));
        ul.appendChild(card)
    });
}

export async function get_sessions(){
    const response = await fetch(`${url}/api/sessions`,{
        method:"GET"
    });
    const sessions = await response.json()
    console.log(sessions)
    render_history(sessions)
}

export async function stop_session(id){
    const response = await fetch(`${url}/api/stop/${id}`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        }
    });
    if (response.ok){
        const data = await response.json()
        console.log(data)
        start_button.disabled=false
    }
}

export async function get_active_session(){
    const response = await fetch(`${url}/api/active-session`)
    if (response.ok){
        const session_data = await response.json()
        if(!session_data || Object.keys(session_data).length === 0){
            start_button.disabled = false
            render_current_session(null)
        }
        else{
            start_button.disabled = true
            render_current_session(session_data)
            console.log(session_data)
        } 
    }
    else{
        start_button.disabled=false
    }
}