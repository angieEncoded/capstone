const viewLicense = async (event, id) => {
    // hide the div that has the customer's data
    document.querySelector(`#clientDetailsRoot`).style.display = "none"
    document.querySelector(`#contactsDetailsRoot`).style.display = "none"
    document.querySelector(`#licensesDetailsRoot`).style.display = "none"

    // get the div that we want to display our data in
    const licenseRoot = document.querySelector(`#licensesEditContent`)

    try {

        // Get the data for the License
        const licenseResults = await fetch(`/get_license/${id}`)
        if (!licenseResults.ok) { throw { status: licenseResults.status, statusText: licenseResults.statusText } }
        const licenseData = await licenseResults.json();
        const licenseJsonData = await JSON.parse(licenseData.data)
        const finalLicenseData = licenseJsonData[0].fields
        const licenseId = licenseJsonData[0].pk
        // populate the form
        const licenseDetails = `
            <div class="container-fluid">
                <h5 class="text-center baskerville-font mb-3">License Information</h5>
                <div class="row">
                    <div class="col-12 col-xl-6">
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Product: </div>
                            <div class="col-10 col-lg-4"><div id="edit-license-product">${finalLicenseData.product === null ? "" : finalLicenseData.product}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-product-icon" class="las la-edit icon-hover" onclick="editLicenseField('product', '${licenseId}', 'textinput')"></i></div>
                        </div>


                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Purchase Date: </div>
                            <div class="col-10 col-lg-4"><div id="edit-license-purchase_date">${finalLicenseData.purchase_date === null ? "" : finalLicenseData.purchase_date}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-purchase_date-icon"  class="las la-edit icon-hover" onclick="editLicenseField('purchase_date', '${licenseId}', 'date')"></i></div>
                        </div>


                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Expiration Date: </div>
                            <div class="col-10 col-lg-4"><div id="edit-license-expiration_date">${finalLicenseData.expiration_date === null ? "" : finalLicenseData.expiration_date} </div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-expiration_date-icon"  class="las la-edit icon-hover" onclick="editLicenseField('expiration_date', '${licenseId}',  'date')"></i></div>
                        </div>


                    </div>
                    <div class="col-12 col-xl-6">


                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">End of Life: </div>
                            <div class="col-10 col-lg-4"><div id="edit-license-end_of_life">${finalLicenseData.end_of_life === null ? "" : finalLicenseData.end_of_life} </div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-end_of_life-icon"  class="las la-edit icon-hover" onclick="editLicenseField('end_of_life', '${licenseId}',  'textinput')"></i></div>
                        </div>


                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">License Key: </div>
                            <div class="col-10 col-lg-4"><div id="edit-license-license_key">${finalLicenseData.license_key === null ? "" : finalLicenseData.license_key} </div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-license_key-icon"  class="las la-edit icon-hover" onclick="editLicenseField('license_key', '${licenseId}',  'textinput')"></i></div>
                        </div>                 
                        
                        
                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">License File: </div>
                            <div class="col-10 col-lg-4 text-truncate">
                                <a href="/download_license/${licenseId}" class="frontend-link" download>${finalLicenseData.license_file === null ? "" : finalLicenseData.license_file}</a>
                                <div id="edit-license-license_file"></div>
                                </div>
                            <div class="col-2 col-lg-4"><i id="edit-license-license_file-icon"  class="las la-edit icon-hover" onclick="editLicenseField('license_file', '${licenseId}',  'file')"></i></div>
                        </div>


                        <div class="row mb-2">
                            <div class="col-4 d-none d-lg-block">Notes</div>
                            <div class="col-10 col-lg-4"><div id="edit-license-notes" class="text-wrap">${finalLicenseData.notes === null ? "" : finalLicenseData.notes}</div></div>
                            <div class="col-2 col-lg-4"><i id="edit-license-notes-icon"  class="las la-edit icon-hover" onclick="editLicenseField('notes', '${licenseId}', 'textarea')"></i></div>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="float-end">
                <button class="btn btn-sm btn-silver" type="button" onclick="closeLicense('${finalLicenseData.customer}')">Back to client</button>
            </div>
        
        `
        // unhide the html root and add the data to ir
        licenseRoot.style.display = "block"
        licenseRoot.innerHTML = licenseDetails


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