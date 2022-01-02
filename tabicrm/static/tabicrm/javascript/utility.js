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
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+={}\-]{2,75}$/
    return re.test(value.trim())
}

const reloadContent = () => {
    location.reload()
}

$(document).ready(function () {
    $('#customersTable').DataTable();
});

$(document).ready(function () {
    $('#contactsTable').DataTable();
});

$(document).ready(function () {
    $('#ticketsTable').DataTable();
});

$(document).ready(function () {
    $('#equipmentTable').DataTable();
});


const viewContactEditForm = (contactId) => {
    window.location.href = `/full_edit_contact/${contactId}`
}

const viewEquipmentEditForm = (equipmentId) => {
    window.location.href = `/full_edit_equipment/${equipmentId}`
}

const viewSingleTicketForm = (ticketId) => {
    window.location.href = `/view_single_ticket/${ticketId}`
}

const viewSingleLicenseForm = (licenseId) => {
    window.location.href = `/full_edit_license/${licenseId}`
}


const openTicketModal = () => {
    let ticketModal = new bootstrap.Modal(document.getElementById('editTicketModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    ticketModal.show()
}

const openHistoryModal = () => {
    let ticketHistoryModal = new bootstrap.Modal(document.getElementById('ticketHistoryModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    ticketHistoryModal.show()
}

const openFullEditForm = () => {
    document.querySelector("#customer-simple-view").style.display = "none"
    document.querySelector("#customer-full-edit-form").style.display = "block"
}

const closeFullEditForm = () => {
    document.querySelector("#customer-simple-view").style.display = "block"
    document.querySelector("#customer-full-edit-form").style.display = "none"
}