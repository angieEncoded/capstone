const quickOpenTicket = async (id) => {

    // get and hide all the other pieces
    document.querySelector(`#clientDetailsRoot`).style.display = "none"
    document.querySelector(`#contactsDetailsRoot`).style.display = "none"
    document.querySelector(`#licensesDetailsRoot`).style.display = "none"
    document.querySelector(`#equipmentDetailsRoot`).style.display = "none"

    // replace the open ticket button with a go back to customer button
    document.querySelector(`#openTicketButton`).style.display = "none"
    document.querySelector(`#closeTicketButton`).style.display = "inline"

    const newTicketFormContainer = document.querySelector(`#newTicketFormContainer`);
    const newTicketFormDetails = document.querySelector(`#newTicketFormDetails`)

    const fullForm =
        `   
        <div class="form-background mb-5">
            <form id="newTicketSubmittedForm" onsubmit="submitNewTicketForm(event, '${id}')" method="POST">
            <div id="newTicketFormDetails">
            ${newTicketFormDetails.innerHTML}
            </div>
            </form>
        </div>  
    `

    // Open the ticket form
    newTicketFormContainer.innerHTML = fullForm
    newTicketFormContainer.style.display = "block"

}


const closeTicketButton = async () => {

    // Show all the other pieces
    document.querySelector(`#clientDetailsRoot`).style.display = "block"
    document.querySelector(`#contactsDetailsRoot`).style.display = "block"
    document.querySelector(`#licensesDetailsRoot`).style.display = "block"
    document.querySelector(`#equipmentDetailsRoot`).style.display = "block"

    // replace the open ticket button with a go back to customer button
    document.querySelector(`#openTicketButton`).style.display = "inline"
    document.querySelector(`#closeTicketButton`).style.display = "none"

    // Close the ticket form
    const newTicketFormContainer = document.querySelector(`#newTicketFormContainer`);

    // Get the existing form
    const existingForm = document.querySelector(`#newTicketFormDetails`)

    const oldCreatedForm =
        `
            <div id="newTicketFormContainer" class="newTicketForm" style="display: none;">
            <div id="newTicketFormDetails">
                ${existingForm.innerHTML}
            </div>
        `

    newTicketFormContainer.innerHTML = oldCreatedForm
    newTicketFormContainer.style.display = "none"
}

const submitNewTicketForm = async (event, id) => {
    event.preventDefault()


    try {
        // Get the data from the form
        const formData = new FormData(document.querySelector('#newTicketSubmittedForm'))

        // Post the data to the back end
        const ticketResults = await fetch(`/post_new_ticket/${id}`, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        if (!ticketResults.ok) { throw { status: ticketResults.status, statusText: ticketResults.statusText } }
        const ticketData = await ticketResults.json()
        if (ticketData.error) { throw ticketData.error }



        if (ticketData.success) {

            // Reset the existing form so we don't have residual data
            const form = document.querySelector(`#newTicketSubmittedForm`)
            form.reset()
            // Show all the other pieces
            document.querySelector(`#clientDetailsRoot`).style.display = "block"
            document.querySelector(`#contactsDetailsRoot`).style.display = "block"
            document.querySelector(`#licensesDetailsRoot`).style.display = "block"
            document.querySelector(`#equipmentDetailsRoot`).style.display = "block"

            // replace the open ticket button with a go back to customer button
            document.querySelector(`#openTicketButton`).style.display = "inline"
            document.querySelector(`#closeTicketButton`).style.display = "none"

            // Close the ticket form
            const newTicketFormContainer = document.querySelector(`#newTicketFormContainer`);

            // Get the existing form
            const existingForm = document.querySelector(`#newTicketFormDetails`)

            const oldCreatedForm =
                `
            <div id="newTicketFormContainer" class="newTicketForm" style="display: none;">
            <div id="newTicketFormDetails">
                ${existingForm.innerHTML}
            </div>
        `

            newTicketFormContainer.innerHTML = oldCreatedForm
            newTicketFormContainer.style.display = "none"

            const successDiv = document.querySelector(`#customer-feedback-data`)
            successDiv.innerHTML = `<span class="text-success">${ticketData.success} (TT-${ticketData.ticket_number})</span>`
            setTimeout(() => {
                successDiv.innerHTML = ""
            }, 10000);
        }


    } catch (error) {
        console.log(error)
        const errorDiv = document.querySelector(`#customer-feedback-data`)
        if (error.status) {
            errorDiv.innerHTML = `<span class="text-danger">${error.status} ${error.statusText}</span>`
        } else {
            errorDiv.innerHTML = `<span class="text-danger">${error}</span>`
        }
        setTimeout(() => {
            errorDiv.innerHTML = ""
        }, 20000);

    }


}

