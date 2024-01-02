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
function increaseFontSize() {
    const button = document.getElementById('increaseButton');
    const currentSize = document.queryCommandValue('fontSize');
    const newSize = parseInt(currentSize) + 1;
    
    document.execCommand('fontSize', false, newSize);
    button.textContent = 'Font Size: ' + newSize;
}

function decreaseFontSize() {
    const button = document.getElementById('decreaseButton');
    const currentSize = document.queryCommandValue('fontSize');
    const newSize = parseInt(currentSize) - 1;

    document.execCommand('fontSize', false, newSize);
    button.textContent = 'Font Size: ' + newSize;
}

function centerText() {
      const isCentered = document.queryCommandState('justifyCenter');
      if (isCentered) {
        document.execCommand('justifyLeft', false, null);
      } else {
        document.execCommand('justifyCenter', false, null);
      }
}


document.getElementById('generatePdfBtn').addEventListener('click', function() {
    var htmlContent = document.getElementById('editor').innerHTML;
    fetch('/generate-pdf', {
          method: 'POST',
          body: JSON.stringify({html_content: htmlContent}),
          headers: {'Content-Type': 'application/json'},
    })
        .then(response => response.blob())
        .then(blob => {
          var url = window.URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url;
          a.download = 'output.pdf';
          a.click();
    })
        .catch(console.error);
});

document.getElementById('uploadPdf').addEventListener('click', function() {
    var pdfFile = document.getElementById('pdfInput').files[0];
    var formData = new FormData();
    formData.append('pdf', pdfFile);
    fetch('/upload-pdf', {
            method: 'POST',
            body: formData,
    })
        .then(response => response.text())
        .then(text => {
            document.getElementById('editor').innerText = text;
        })
        .catch(console.error);
});