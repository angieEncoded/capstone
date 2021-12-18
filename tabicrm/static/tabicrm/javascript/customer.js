// From Django documentation how to get the csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up a simple regex to check the contents of the post
const textCheck = (value) => {
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+={}\-]{5,75}$/
    return re.test(value.trim())
}

const reloadContent = () => {
    location.reload()
}

const editField = async (fieldName, id, currentData, fieldType) => {
    let editTemplate;
    // create the edit form
    if (fieldType === "textarea") {
        editTemplate = `
        <form onsubmit="submitForm(event,'${id}', '${fieldName}')">
            <textarea class="form-control mb-2 form-control-sm" id="input-${fieldName}">${currentData}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    } else {
        editTemplate = `
        <form onsubmit="submitForm(event,'${id}', '${fieldName}')">
            <input type="text" class="form-control mb-2 form-control-sm" value='${currentData}' id="input-${fieldName}" maxlength=255 />
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
            </div>
        </form>
        `
    }

    // insert the form into the div
    const currentEditField = document.querySelector(`#edit-${fieldName}`)
    currentEditField.innerHTML = editTemplate
}

const submitForm = async (event, id, fieldName) => {
    event.preventDefault() // stop any propegation

    // Get the data from the form
    const data = document.querySelector(`#input-${fieldName}`)
    const submission = {
        [fieldName]: data.value // use [] for a json key variable
    }

    try {
        // Send the request to the back end to update the data
        const results = await fetch(`/edit_customer/${id}/${fieldName}`, {
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
            document.querySelector(`#edit-${fieldName}`).innerHTML = data.content
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

// Close the small editing form
const cancelEdit = (fieldName, currentData) => {
    document.querySelector(`#edit-${fieldName}`).innerHTML = currentData
}

const viewClient = async (id) => {
    let customerModal = new bootstrap.Modal(document.getElementById('clientDetails'), {
        keyboard: false,
        backdrop: 'static'
    })

    // Grab data from the back end
    try {



        // Get the customer data
        const customerResults = await fetch(`/view_customer/${id}`)
        if (!customerResults.ok) { throw { status: customerResults.status, statusText: customerResults.statusText } }
        const customerData = await customerResults.json();
        const customerJsonData = await JSON.parse(customerData.data) // Coming back from python just sucks
        const finalData = customerJsonData[0].fields
        const customerId = customerJsonData[0].pk


        // Get the contacts data
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
                <tr class="select-customer" id="${contactsJsonData[i].pk}" onclick="editContact('${contactsJsonData[i].pk}')">
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






        // Create an element for the data
        const customerDetailsForm =
            `
            <div class="container-fluid">
            <!-- Notes -->
            <div class="row mb-2">
                <div class="col-4 d-none d-lg-block">Notes</div>
                <div class="col-10 col-lg-4"><div id="edit-notes">${finalData.notes}</div></div>
                <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('notes', '${customerId}', '${finalData.notes}', 'textarea')"></i></div>
            </div>
            <hr>
            <!-- BASIC INFORMATION -->
            <h5 class="text-center baskerville-font mb-3">Basic Information</h5>
            <div class="row">
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Customer Name: </div>
                        <div class="col-10 col-lg-4"><div id="edit-name">${finalData.name}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('name', '${customerId}', '${finalData.name}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Primary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-primary_phone">${finalData.primary_phone}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('primary_phone', '${customerId}', '${finalData.primary_phone}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Secondary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-secondary_phone">${finalData.secondary_phone} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('secondary_phone', '${customerId}', '${finalData.secondary_phone}', 'textinput')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Fax: </div>
                        <div class="col-10 col-lg-4"><div id="edit-fax">${finalData.fax} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('fax', '${customerId}', '${finalData.fax}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Website: </div>
                        <div class="col-10 col-lg-4"><div id="edit-website">${finalData.website} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('website', '${customerId}', '${finalData.website}', 'textinput')"></i></div>
                    </div>
                </div>
            </div>
        
            <!-- BILLING ADDRESS -->
            <h5 class="text-center baskerville-font mb-3">Billing Address</h5>
            <div class="row">
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address One:</div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_one">${finalData.billing_address_one} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_one', '${customerId}', '${finalData.billing_address_one}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_two">${finalData.billing_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_two', '${customerId}', '${finalData.billing_address_two}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_city">${finalData.billing_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_city', '${customerId}', '${finalData.billing_address_city}', 'textinput')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_state">${finalData.billing_address_state}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_state', '${customerId}', '${finalData.billing_address_state}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_zip">${finalData.billing_address_zip}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_zip', '${customerId}', '${finalData.billing_address_zip}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_country">${finalData.billing_address_country}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_country', '${customerId}', '${finalData.billing_address_country}', 'textinput')"></i></div>
                    </div>
                </div>
            </div>

            <!-- SHIPPING ADDRESS -->
            <h5 class="text-center baskerville-font mb-3">Shipping Address</h5>
            <div class="row">
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address One: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_one">${finalData.shipping_address_one} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_one', '${customerId}', '${finalData.shipping_address_one}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_two">${finalData.shipping_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_two', '${customerId}', '${finalData.shipping_address_two}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_city">${finalData.shipping_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_city', '${customerId}', '${finalData.shipping_address_city}', 'textinput')"></i></div>
                    </div>
        
        
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_state">${finalData.shipping_address_state} </div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_state', '${customerId}', '${finalData.shipping_address_state}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_zip">${finalData.shipping_address_zip}</div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_zip', '${customerId}', '${finalData.shipping_address_zip}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_country">${finalData.shipping_address_country} </div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_country', '${customerId}', '${finalData.shipping_address_country}', 'textinput')"></i></div>
                    </div>
        
                </div>
            </div>
        </div>
        <hr>
        `

        const customerFullDetails = `
            ${customerDetailsForm}
            ${customerContactsTable}
        `

        // Populate the modal's data
        const modalTitle = document.querySelector(`#clientDetailsTitle`)
        modalTitle.innerHTML = `Viewing details for: ${finalData.name}`
        const clientDetails = document.querySelector(`#clientDetailsContent`)
        clientDetails.innerHTML = customerFullDetails

        // Open the modal
        customerModal.show()
    } catch (error) {
        const errorDiv = document.querySelector(`#feedbackContainer`)
        errorDiv.innerHTML = `
            <div class="text-center alert alert-danger alert-dismissible fade show" role="alert">
            ${error.status} ${error.statusText}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `
    }
}


































