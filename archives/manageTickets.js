const openCommentForm = (ticketId) => {
    const commentButton = document.querySelector(`#add-comment-button`)
    const commentRoot = document.querySelector(`#comment-root`)
    const commentTemplate = `
    <form onsubmit="submitAddComment(event, '${ticketId}')">
        <textarea class="form-control mb-2 form-control-sm" id="add-comment" rows="8"></textarea>
        <div class="float-end">
        <button class="btn btn-sm btn-logo" type="submit">Save</button>
        <button class="btn btn-sm btn-silver" type="button" onclick="cancelAddComment()">Cancel</button>
        </div>
    </form>
    `
    commentRoot.innerHTML = commentTemplate;
    commentButton.style.visibility = 'hidden'
}

const cancelAddComment = () => {
    const commentButton = document.querySelector(`#add-comment-button`)
    const commentRoot = document.querySelector(`#comment-root`)
    commentButton.style.visibility = 'visible'
    commentRoot.innerHTML = ""
}