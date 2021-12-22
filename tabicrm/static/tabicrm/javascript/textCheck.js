// Set up a simple regex to check the contents of the post
const textCheck = (value) => {
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+={}\-]{2,75}$/
    return re.test(value.trim())
}