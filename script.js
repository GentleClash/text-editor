function toggleBold() {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const isBold = range.startContainer.parentNode.tagName === 'B';
    const button = document.getElementById('boldButton');

    if (isBold) {
        document.execCommand('bold', false, null);
        button.textContent = 'Bold | Off';
    } else {
        document.execCommand('bold', true, null);
        button.textContent = 'Bold | On';
    }
}

function toggleItalic() {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const isItalic = range.startContainer.parentNode.tagName === 'I';
    const button = document.getElementById('italicButton');
    if (isItalic) {
        document.execCommand('italic', false, null);
        button.textContent = 'Italic | Off';
    } else {
        document.execCommand('italic', true, null);
        button.textContent = 'Italic | On';
    }
}

function toggleUnderline() {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const isUnderline = range.startContainer.parentNode.tagName === 'U';
    const button = document.getElementById('underlineButton');

    if (isUnderline) {
        document.execCommand('underline', false, null);
        button.textContent = 'Underline | Off';
    } else {
        document.execCommand('underline', true, null);
        button.textContent = 'Underline | On';
    }
}