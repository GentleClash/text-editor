## Overview

Web application designed for efficient text editing and manipulation.





## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Working](#working)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Text Formatting:** Apply formatting such as bold, italic, underline, and adjust font size to enhance the appearance of your text.
- **Text Manipulation:** Paraphrase text to convey the same meaning in different words. Upload PDFs and convert them to editable text seamlessly.
- **Document Summarization:** Generate concise summaries of documents with just a click.
- **PDF Generation:** Save your edited or summarized content as PDF files for easy sharing and storage.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GentleClash/text-editor.git
   ```

2. Navigate to the project directory:

   ```bash
   cd text-editor
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   - Create a `.env` file in the project root.
   - Add the environment variable `API_KEY`.
   - Example:

     ```env
     API_KEY=your_api_key_here
     ```

   - Save the file.

## Usage

1. Run the Flask app:

   ```bash
   python app.py
   ```

2. Open a web browser and go to [http://localhost:5000/](http://localhost:5000/) to access the app.

3. Use the toolbar and features to edit and manipulate text as needed.

## Working

1. **Text Editing:** Use the toolbar to apply various formatting options to your text.
2. **Paraphrasing:** Select the text and click the "Paraphrase" button to obtain a rephrased version of your text.
3. **PDF Conversion:** Upload PDFs using the provided interface and convert them to editable text.
4. **Document Summarization:** Summarize your documents effortlessly.
5. **PDF Generation:** Save your edited or summarized text as a PDF file.

## Contributing

If you would like to contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the [LICENSE](LICENSE).
