const viewCustomer = async (id) => {

    // Hide the editing root for the contacts if needed
    document.querySelector(`#contactsEditContent`).style.display = "none"
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
        const customerJsonData = await JSON.parse(customerData.data)
        const finalData = customerJsonData[0].fields
        const customerId = customerJsonData[0].pk


        // Get the contacts data
        const contactsResults = await fetch(`/get_customer_contacts/${id}`)
        if (!contactsResults.ok) { throw { status: contactsResults.status, statusText: contactsResults.statusText } }
        const contactsData = await contactsResults.json();
        const contactsJsonData = await JSON.parse(contactsData.data)

        // Get the licenses data
        const licenseResults = await fetch(`/get_customer_licenses/${id}`)
        if (!licenseResults.ok) { throw { status: licenseResults.status, statusText: licenseResults.statusText } }
        const licenseData = await licenseResults.json();
        const licenseJsonData = await JSON.parse(licenseData.data)

        // Get the equipment data
        const equipmentResults = await fetch(`/get_customer_equipment/${id}`)
        if (!equipmentResults.ok) { throw { status: equipmentResults.status, statusText: equipmentResults.statusText } }
        const equipmentData = await equipmentResults.json();
        const equipmentJsonData = await JSON.parse(equipmentData.data)

        // Set up the string for injecting into the DOM
        let customerContactsTable = ''
        let tableEntries = ''
        let customerLicensesTable = ''
        let licenseEntries = ''
        let customerEquipmentTable = ''
        let equipmentEntries = ''

        // Process Contacts Data
        if (contactsJsonData.length > 0) {
            // With a for loop, add the data fields to a table
            for (i = 0; i < contactsJsonData.length; i++) {
                tableEntries += `
                <tr class="select-customer" id="${contactsJsonData[i].pk}" onclick="viewContact(event, '${contactsJsonData[i].pk}')">
                    <td>${contactsJsonData[i].fields.first_name === null || contactsJsonData[i].fields.first_name === undefined ? "" : contactsJsonData[i].fields.first_name}</td>
                    <td>${contactsJsonData[i].fields.last_name === null || contactsJsonData[i].fields.last_name === undefined ? "" : contactsJsonData[i].fields.last_name}</td>
                    <td>${contactsJsonData[i].fields.job_title === null || contactsJsonData[i].fields.job_title === undefined ? "" : contactsJsonData[i].fields.job_title}</td>
                    <td>${contactsJsonData[i].fields.extension === null || contactsJsonData[i].fields.extension === undefined ? "" : contactsJsonData[i].fields.extension}</td>
                    <td  class="text-truncate"  style="max-width: 150px;">${contactsJsonData[i].fields.notes === null || contactsJsonData[i].fields.notes === undefined ? "" : contactsJsonData[i].fields.notes}</td>
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
            customerContactsTable = `
            <h5 class="text-center baskerville-font mb-3">Contacts</h5>
            <p class="text-center">No contacts recorded for this customer.</p>
            `
        }


        // Process License Data
        if (licenseJsonData.length > 0) {
            // With a for loop, add the data fields to a table
            for (i = 0; i < licenseJsonData.length; i++) {
                licenseEntries += `
                <tr id="${licenseJsonData[i].pk}">
                    <td>${licenseJsonData[i].fields.product === null || licenseJsonData[i].fields.product === undefined ? "" : licenseJsonData[i].fields.product}</td>
                    <td>${licenseJsonData[i].fields.purchase_date === null || licenseJsonData[i].fields.purchase_date === undefined ? "" : licenseJsonData[i].fields.purchase_date}</td>
                    <td>${licenseJsonData[i].fields.expiration_date === null || licenseJsonData[i].fields.expiration_date === undefined ? "" : licenseJsonData[i].fields.expiration_date}</td>
                    <td>${licenseJsonData[i].fields.license_key === null || licenseJsonData[i].fields.license_key === undefined ? "" : licenseJsonData[i].fields.license_key}</td>
                    <td class="text-truncate"  style="max-width: 50px;">
                        <a href="/download_license/${licenseJsonData[i].pk}" class="frontend-link" download>
                        ${licenseJsonData[i].fields.license_file === null || licenseJsonData[i].fields.license_file === undefined ? "" : licenseJsonData[i].fields.license_file}
                        </a>
                    </td>
                    <!--
                    <td class="select-customer">
                        <a href="/edit_license/${licenseJsonData[i].pk}" class="frontend-link">
                            <div class="full-expand text-center">
                                <i class="las la-edit"></i>
                            </div>
                        </a>
                    </td> 
                    -->
                    </tr>
                \n
                `
            }
            customerLicensesTable =
                `
                <!-- CONTACT INFORMATION -->
                <h5 class="text-center baskerville-font mb-3">License Information</h5>
                <table class="table table-responsive">
                    <thead class="thead-dark">
                        <tr>
                            <th scope="col">Product</th>
                            <th scope="col">Purchase Date</th>
                            <th scope="col">Expiration Date</th>
                            <th scope="col">License Key</th>
                            <th scope="col">License File</th>
                           <!-- <th scope="col"  class="text-center">Edit Form</th> -->
                        </tr>
                    </thead>
                    <tbody>
                        ${licenseEntries}
                    </tbody>
                </table>
                `
        } else {
            customerLicensesTable = `
            <h5 class="text-center baskerville-font mb-3">License Information</h5>
            <p class="text-center">No licenses recorded for this customer.</p>
            `
        }


        // Process Equipment Data
        if (equipmentJsonData.length > 0) {
            // With a for loop, add the data fields to a table
            for (i = 0; i < equipmentJsonData.length; i++) {
                equipmentEntries += `
                <tr id="${equipmentJsonData[i].pk}")">
                    <td>${equipmentJsonData[i].fields.type === null || equipmentJsonData[i].fields.type === undefined ? "" : equipmentJsonData[i].fields.type}</td>
                    <td>${equipmentJsonData[i].fields.vendor === null || equipmentJsonData[i].fields.vendor === undefined ? "" : equipmentJsonData[i].fields.vendor}</td>
                    <td>${equipmentJsonData[i].fields.model === null || equipmentJsonData[i].fields.model === undefined ? "" : equipmentJsonData[i].fields.model}</td>
                    <td>${equipmentJsonData[i].fields.internal_ip_address === null || equipmentJsonData[i].fields.internal_ip_address === undefined ? "" : equipmentJsonData[i].fields.internal_ip_address}</td>
                    <td>${equipmentJsonData[i].fields.external_ip_address === null || equipmentJsonData[i].fields.external_ip_address === undefined ? "" : equipmentJsonData[i].fields.external_ip_address}</td>
                    <td>${equipmentJsonData[i].fields.serial === null || equipmentJsonData[i].fields.serial === undefined ? "" : equipmentJsonData[i].fields.serial}</td>
                </tr>
                    \n
                `
            }
            customerEquipmentTable =
                `
                <!-- EQUIPMENT INFORMATION -->
                <h5 class="text-center baskerville-font mb-3">Equipment</h5>
                <table class="table  table-striped table-responsive">
                    <thead class="thead-dark">
                        <tr>
                            <th scope="col">Type</th>
                            <th scope="col">Vendor</th>
                            <th scope="col">Model</th>
                            <th scope="col">Internal IP Address</th>
                            <th scope="col">External IP Address</th>
                            <th scope="col">Serial #</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${equipmentEntries}
                    </tbody>
                </table>
                `
        } else {
            customerEquipmentTable = `
            <h5 class="text-center baskerville-font mb-3">Equipment</h5>
            <p class="text-center">No equipment recorded for this customer.</p>
            `
        }




        // Create an element for the data
        const customerDetailsForm =
            `
            <div class="container-fluid">
            <!-- Notes -->
            <div class="row mb-2">
                <div class="col-4 d-none d-lg-block">Notes</div>
                <div class="col-10 col-lg-4"><div id="edit-notes" class="text-wrap">${finalData.notes === null ? "" : finalData.notes}</div></div>
                <div class="col-2 col-lg-4"><i id="edit-notes-icon" class="las la-edit icon-hover" onclick="editField('notes', '${customerId}', 'textarea')"></i></div>

            </div>

          
            <hr>
            <!-- BASIC INFORMATION -->
            <h5 class="text-center baskerville-font mb-3">Basic Information</h5>
            <div class="row">
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Customer Name: </div>
                        <div class="col-10 col-lg-4"><div id="edit-name">${finalData.name}</div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-name-icon"class="las la-edit icon-hover" onclick="editField('name', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Primary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-primary_phone">${finalData.primary_phone}</div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-primary_phone-icon" class="las la-edit icon-hover" onclick="editField('primary_phone', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Secondary Phone: </div>
                        <div class="col-10 col-lg-4"><div id="edit-secondary_phone">${finalData.secondary_phone} </div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-secondary_phone-icon"class="las la-edit icon-hover" onclick="editField('secondary_phone', '${customerId}', 'textinput')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Fax: </div>
                        <div class="col-10 col-lg-4"><div id="edit-fax">${finalData.fax} </div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-fax-icon"class="las la-edit icon-hover" onclick="editField('fax', '${customerId}','textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Website: </div>
                        <div class="col-10 col-lg-4"><div id="edit-website">${finalData.website} </div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-website-icon" class="las la-edit icon-hover" onclick="editField('website', '${customerId}', 'textinput')"></i></div>
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
                        <div class="col-2 col-lg-4"><i  id="edit-billing_address_one-icon" class="las la-edit icon-hover" onclick="editField('billing_address_one', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_two">${finalData.billing_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i   id="edit-billing_address_two-icon" class="las la-edit icon-hover" onclick="editField('billing_address_two', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_city">${finalData.billing_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i   id="edit-billing_address_city-icon" class="las la-edit icon-hover" onclick="editField('billing_address_city', '${customerId}', 'textinput')"></i></div>
                    </div>
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_state">${finalData.billing_address_state}</div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-billing_address_state-icon" class="las la-edit icon-hover" onclick="editField('billing_address_state', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_zip">${finalData.billing_address_zip}</div></div>
                        <div class="col-2 col-lg-4"><i id="edit-billing_address_zip-icon" class="las la-edit icon-hover" onclick="editField('billing_address_zip', '${customerId}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Billing Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-billing_address_country">${finalData.billing_address_country}</div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-billing_address_country-icon" class="las la-edit icon-hover" onclick="editField('billing_address_country', '${customerId}', 'textinput')"></i></div>
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
                        <div class="col-2 col-lg-4"><i id="edit-shipping_address_one-icon" class="las la-edit icon-hover" onclick="editField('shipping_address_one', '${customerId}', '${finalData.shipping_address_one}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Two: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_two">${finalData.shipping_address_two} </div></div>
                        <div class="col-2 col-lg-4"><i  id="edit-shipping_address_two-icon" class="las la-edit icon-hover" onclick="editField('shipping_address_two', '${customerId}', '${finalData.shipping_address_two}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address City: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_city">${finalData.shipping_address_city} </div></div>
                        <div class="col-2 col-lg-4"><i id="edit-shipping_address_city-icon"  class="las la-edit icon-hover" onclick="editField('shipping_address_city', '${customerId}', '${finalData.shipping_address_city}', 'textinput')"></i></div>
                    </div>
        
        
                </div>
                <div class="col-12 col-xl-6">
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address State: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_state">${finalData.shipping_address_state} </div> </div>
                        <div class="col-2 col-lg-4"><i id="edit-shipping_address_state-icon"  class="las la-edit icon-hover" onclick="editField('shipping_address_state', '${customerId}', '${finalData.shipping_address_state}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Zip: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_zip">${finalData.shipping_address_zip}</div> </div>
                        <div class="col-2 col-lg-4"><i id="edit-shipping_address_zip-icon"  class="las la-edit icon-hover" onclick="editField('shipping_address_zip', '${customerId}', '${finalData.shipping_address_zip}', 'textinput')"></i></div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-4 d-none d-lg-block">Shipping Address Country: </div>
                        <div class="col-10 col-lg-4"><div id="edit-shipping_address_country">${finalData.shipping_address_country} </div> </div>
                        <div class="col-2 col-lg-4"><i id="edit-shipping_address_country-icon" class="las la-edit icon-hover" onclick="editField('shipping_address_country', '${customerId}', '${finalData.shipping_address_country}', 'textinput')"></i></div>
                    </div>
        
                </div>
            </div>
        </div>
        <hr>
        `

        // Populate the modal's data
        const modalTitle = document.querySelector(`#clientDetailsTitle`)
        modalTitle.innerHTML = `
            ${finalData.name}
            <a href="/customer_full_form/${id}" class="btn-sm btn-silver ms-5">Full Details</a>
            <button id="openTicketButton" class="btn-sm btn-silver ms-2" onclick="quickOpenTicket('${id}')" style="display: inline;">Open Ticket</button>
            <a id="closeTicketButton" href="#" class="btn-sm btn-silver ms-2" onclick="closeTicketButton('${id}');return false;" style="display: none;">Back to customer</a>
            <a href="/display_tickets/${id}" class="btn-sm btn-silver ms-2">All customer tickets</a>
        `
        const clientDetails = document.querySelector(`#clientDetailsRoot`)
        clientDetails.innerHTML = customerDetailsForm

        // Find the root for the contacts content
        const contactsRoot = document.querySelector(`#contactsDetailsRoot`)
        contactsRoot.innerHTML = customerContactsTable

        // Find the root for the licenses content
        const licensesRoot = document.querySelector(`#licensesDetailsRoot`)
        licensesRoot.innerHTML = customerLicensesTable

        // Find the root for the equipment content
        const equipmentRoot = document.querySelector(`#equipmentDetailsRoot`)
        equipmentRoot.innerHTML = customerEquipmentTable


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