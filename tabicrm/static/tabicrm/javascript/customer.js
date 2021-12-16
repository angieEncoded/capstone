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


const editField = async (fieldName, id, currentData) => {
    // create the edit form
    const editTemplate = `
    <form onsubmit="submitForm(event, ${id})">
        <input type="text" class="form-control mb-2 form-control-sm" value='${currentData}' id="input-${fieldName}" maxlength=255 />
        <div class="float-end">
        <button class="btn btn-sm btn-logo" type="submit">Save</button>
        <button class="btn btn-sm btn-silver" type="button" onclick="cancelEdit('${fieldName}', '${currentData}' )">Cancel</button>
        </div>
    </form>
    `

    // insert the form into the div
    const currentEditField = document.querySelector(`#edit-${fieldName}`)
    currentEditField.innerHTML = editTemplate
}

// Close the small editing form
const cancelEdit = (fieldName, currentData) => {
    document.querySelector(`#edit-${fieldName}`).innerHTML = currentData
}

// Set up the modal html
// 

const viewClient = async (id) => {
    let customerModal = new bootstrap.Modal(document.getElementById('clientDetails'), {
        keyboard: false
    })

    // Grab data from the back end
    try {
        const results = await fetch(`/view_customer/${id}`)
        if (!results.ok) { throw { status: results.status, statusText: results.statusText } }

        const customerData = await results.json();
        const jsonData = JSON.parse(customerData.data) // Coming back from python just sucks
        const finalData = jsonData[0].fields
        const customerId = jsonData[0].pk

        // Create an element for the data
        const customerDetailsForm =
            `
            <div class="container-fluid">
            <!-- BASIC INFORMATION -->
            <h5 class="text-center baskerville-font mb-3">Basic Information</h5>
            <div class="row">
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Customer Name: </div>
                        <div class="col-10 col-lg-4"><div id="edit-name">${finalData.name}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('name', '${customerId}', '${finalData.name}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Primary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-primary_phone">${finalData.primary_phone}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('primary_phone', '${customerId}', '${finalData.primary_phone}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Secondary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-secondary_phone">${finalData.secondary_phone} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('secondary_phone', '${customerId}', '${finalData.secondary_phone}')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Fax: </div>
                        <div class="col-10 col-lg-4"><div id="edit-fax">${finalData.fax} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('fax', '${customerId}', '${finalData.fax}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Website: </div>
                        <div class="col-10 col-lg-4"><div id="edit-website">${finalData.website} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('website', '${customerId}', '${finalData.website}')"></i></div>
                    </div>
                </div>
            </div>
        
            <!-- BILLING ADDRESS -->
            <h5 class="text-center baskerville-font mb-3">Billing Address</h5>
            <div class="row">
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address One:</div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_one">${finalData.billing_address_one} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_one', '${customerId}', '${finalData.billing_address_one}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_two">${finalData.billing_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_two', '${customerId}', '${finalData.billing_address_two}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_city">${finalData.billing_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_city', '${customerId}', '${finalData.billing_address_city}')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_state">${finalData.billing_address_state}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_state', '${customerId}', '${finalData.billing_address_state}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_zip">${finalData.billing_address_zip}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_zip', '${customerId}', '${finalData.billing_address_zip}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_country">${finalData.billing_address_country}</div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('billing_address_country', '${customerId}', '${finalData.billing_address_country}')"></i></div>
                    </div>
                </div>
            </div>
        
        
            <!-- SHIPPING ADDRESS -->
            <h5 class="text-center baskerville-font mb-3">Shipping Address</h5>
            <div class="row">
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address One: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_one">${finalData.shipping_address_one} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_one', '${customerId}', '${finalData.shipping_address_one}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_two">${finalData.shipping_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_two', '${customerId}', '${finalData.shipping_address_two}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_city">${finalData.shipping_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_city', '${customerId}', '${finalData.shipping_address_city}')"></i></div>
                    </div>
        
        
                </div>
                <div class="col-12 col-lg-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_state">${finalData.shipping_address_state} </div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_state', '${customerId}', '${finalData.shipping_address_state}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_zip">${finalData.shipping_address_zip}</div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_zip', '${customerId}', '${finalData.shipping_address_zip}')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_country">${finalData.shipping_address_country} </div> </div>
                        <div class="col-2 col-lg-4"><i class="las la-edit icon-hover" onclick="editField('shipping_address_country', '${customerId}', '${finalData.shipping_address_country}')"></i></div>
                    </div>
        
                </div>
            </div>
        </div>
        `

        // Populate the modal's data
        const modalTitle = document.querySelector(`#clientDetailsTitle`)
        modalTitle.innerHTML = `Viewing details for: ${finalData.name}`
        const clientDetails = document.querySelector(`#clientDetailsContent`)
        clientDetails.innerHTML = customerDetailsForm

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