

// close button WORK ON HOW TO RELOAD FROM CHANGES IN THE OTHER PAGE
const closeContact = async (event, id) => {

    // hide the div that has the customer's data
    document.querySelector(`#clientDetailsContent`).style.display = "block"

    // get the div that we want to display our data in
    const contactsRoot = document.querySelector(`#contactsEditContent`)
    contactsRoot.innerHTML = ""
    contactsRoot.style.display = "none"
}


const editContactField = async (fieldName, id, currentData, fieldType) => {
    let editTemplate;
    // create the edit form
    if (fieldType === "textarea") {
        editTemplate = `
        <form onsubmit="submitEditContactForm(event,'${id}', '${fieldName}')">
            <textarea class="form-control mb-2 form-control-sm" id="contact-input-${fieldName}">${currentData === 'null' ? "" : currentData}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelContactEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    } else {
        editTemplate = `
        <form onsubmit="submitEditContactForm(event,'${id}', '${fieldName}')">
            <input type="text" class="form-control mb-2 form-control-sm" value='${currentData === 'null' ? "" : currentData}' id="contact-input-${fieldName}" maxlength=255 />
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelContactEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // insert the form into the div
    const currentEditField = document.querySelector(`#edit-contact-${fieldName}`)
    currentEditField.innerHTML = editTemplate
}



// Close the small editing form
const cancelContactEdit = (fieldName, currentData) => {
    document.querySelector(`#edit-contact-${fieldName}`).innerHTML = currentData
}


const submitEditContactForm = async (event, id, fieldName) => {
    event.preventDefault() // stop any propegation

    // Get the data from the form
    const data = document.querySelector(`#contact-input-${fieldName}`)
    const submission = {
        [fieldName]: data.value // use [] for a json key variable
    }

    try {
        // Send the request to the back end to update the data
        const results = await fetch(`/edit_contact/${id}/${fieldName}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        if (!results.ok) { throw { status: results.status, statusText: results.statusText } }
        const data = await results.json()

        // If the server sent back an error because we did something wrong
        if (data.error) { throw data.error }

        if (data.success) {
            const successDiv = document.querySelector(`#customer-feedback-data`)
            successDiv.innerHTML = `<span class="text-success">${data.success}</span>`
            document.querySelector(`#edit-contact-${fieldName}`).innerHTML = data.content
        }
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




























