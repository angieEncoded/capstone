const closeContact = async (id) => {

    // Get the details about the contact again and build the list
    const contactsResults = await fetch(`/get_customer_contacts/${id}`)
    if (!contactsResults.ok) { throw { status: contactsResults.status, statusText: contactsResults.statusText } }
    const contactsData = await contactsResults.json();
    const contactsJsonData = await JSON.parse(contactsData.data)


    let customerContactsTable = ''
    let tableEntries = ''

    // If we do have data, we need to process it
    if (contactsJsonData.length > 0) {
        // With a for loop, add the data fields to a table
        for (i = 0; i < contactsJsonData.length; i++) {
            tableEntries += `
                    <tr class="select-customer" id="${contactsJsonData[i].pk}" onclick="viewContact(event, '${contactsJsonData[i].pk}')">
                        <td>${contactsJsonData[i].fields.first_name === null ? "" : contactsJsonData[i].fields.first_name}</td>
                        <td>${contactsJsonData[i].fields.last_name === null ? "" : contactsJsonData[i].fields.last_name}</td>
                        <td>${contactsJsonData[i].fields.job_title === null ? "" : contactsJsonData[i].fields.job_title}</td>
                        <td>${contactsJsonData[i].fields.extension === null ? "" : contactsJsonData[i].fields.extension}</td>
                        <td>${contactsJsonData[i].fields.notes === null ? "" : contactsJsonData[i].fields.notes}</td>
                    </tr>
                    \n
                    `
        }
        customerContactsTable =
            `
                    <!-- CONTACT INFORMATION -->
                    <h5 class="text-center baskerville-font mb-3">Contacts</h5>
                    <table class="table  table-striped table-responsive">
                        <thead class="thead-dark">
                            <tr>
                                <th scope="col">First Name</th>
                                <th scope="col">Last Name</th>
                                <th scope="col">Job Title</th>
                                <th scope="col">Extension</th>
                                <th scope="col">Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableEntries}
                        </tbody>
                    </table>
                    `
    } else {
        customerContactsTable = `No contacts recorded for this customer.`
    }


    // show the div that has the customer's data
    document.querySelector(`#clientDetailsRoot`).style.display = "block"

    // replace the content in the bottom div that has the contact information
    const contactsRoot = document.querySelector(`#contactsDetailsRoot`)
    contactsRoot.innerHTML = customerContactsTable
    contactsRoot.style.display = "block"

    // show the licenses again
    const licensesRoot = document.querySelector(`#licensesDetailsRoot`)
    licensesRoot.style.display = "block"


    // Hide our old stuff
    const contactsEditRoot = document.querySelector(`#contactsEditContent`)
    contactsEditRoot.innerHTML = ""
    contactsEditRoot.style.display = "none"




}

const editContactField = async (fieldName, id, fieldType) => {
    let editTemplate = "";
    // create the edit form

    // Hide the editing button to fix a bug
    const editButton = document.querySelector(`#edit-contact-${fieldName}-icon`)
    editButton.style.display = "none"

    // GEt the current data from what is in the inner html
    const currentEditField = document.querySelector(`#edit-contact-${fieldName}`)
    const currentData = currentEditField.innerHTML



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
    currentEditField.innerHTML = editTemplate
}



// Close the small editing form
const cancelContactEdit = (fieldName, currentData) => {
    const editButton = document.querySelector(`#edit-contact-${fieldName}-icon`)
    editButton.style.display = "block"
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
            const editButton = document.querySelector(`#edit-contact-${fieldName}-icon`)
            editButton.style.display = "block"
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