
// close button WORK ON HOW TO RELOAD FROM CHANGES IN THE OTHER PAGE
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