const quickOpenTicket = async (id) => {

    // get and hide all the other pieces
    document.querySelector(`#clientDetailsRoot`).style.display = "none"
    document.querySelector(`#contactsDetailsRoot`).style.display = "none"
    document.querySelector(`#licensesDetailsRoot`).style.display = "none"
    document.querySelector(`#equipmentDetailsRoot`).style.display = "none"

    // replace the open ticket button with a go back to customer button
    document.querySelector(`#openTicketButton`).style.display = "none"
    document.querySelector(`#closeTicketButton`).style.display = "inline"

    // get the div that we want to display our data in
    const quickOpenTicketRoot = document.querySelector(`#quickOpenTicketContent`)


    try {

        const formResults = await fetch("/get_ticket_form/0")
        if (!formResults.ok) { throw { status: formResults.status, statusText: formResults.statusText } }
        const jsonFormResults = await formResults.json()
        console.log(jsonFormResults)


        const newTicketForm = `
        sfsafsfdsa
        
        `
        // unhide the html root and add the data to it
        quickOpenTicketRoot.style.display = "block"
        quickOpenTicketRoot.innerHTML = newTicketForm


    } catch (error) {
        console.log(error)
        const errorDiv = document.querySelector(`#customer-feedback-data`)
        if (error.status) {
            errorDiv.innerHTML = `<span class="text-danger">${error.status} ${error.statusText}</span>`
        } else {
            errorDiv.innerHTML = `<span class="text-danger">${error}</span>`
        }
    }




}


const closeTicketButton = async () => {


    // replace the open ticket button with a go back to customer button
    document.querySelector(`#openTicketButton`).style.display = "inline"
    document.querySelector(`#closeTicketButton`).style.display = "none"


    document.querySelector(`#quickOpenTicketContent`).style.display = "none"
    document.querySelector(`#clientDetailsRoot`).style.display = "block"
    document.querySelector(`#contactsDetailsRoot`).style.display = "block"
    document.querySelector(`#licensesDetailsRoot`).style.display = "block"
    document.querySelector(`#equipmentDetailsRoot`).style.display = "block"
}