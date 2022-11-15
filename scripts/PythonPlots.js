// All code runs in this anonymous function
// to avoid cluttering the global variables
(function() {

  // python code to run at startup
  let startupCode = `
import sys, io
sys.stdout = io.StringIO() # redirect stdout
def create_root_element1(self):
    div = document.createElement('div')
    document.getElementById("pyplotdiv").appendChild(div)
    return div
import matplotlib.pyplot as plt
from matplotlib.backends import backend_agg
from js import document
`;

  // Create a CodeMirror instance
  let myCodeMirror = CodeMirror(document.getElementById("codeEditor"), {
    mode:  "python",
    lineNumbers: true
  } );

  // Minimal script requirements
  let requiredLines = [
    "# Open this file with jeroenvantilburg.nl/ppg or any python environment",
    "import matplotlib.pyplot as plt",
    "plt.show()" ] ;
  let markOptions = { css: "opacity: 0.5;", readOnly: true, inclusiveLeft: true };

  // Run the script when user clicks on Run button
  $("#runCode").click( evaluatePython );

  // Read the xml file from the hash of the web address
  function readFileFromHash() {
    let pyFile = window.location.hash.substr(1);
  
    if( pyFile == "") { // If hash is empty show the Gallery
      showModal("galleryModal");
      return;
    }
    else if ( pyFile.includes("https") ) {
      console.log("Trying to load external python file");
      $.get(pyFile, function(data) {
        console.log(pyFile);
        console.log(data);
      });
    } else {
      pyFile = "gallery/"+pyFile;
    }
  
    // Load the python file
    loadScript( pyFile );  
  }

  // Trigger reload when hash has changed
  $(window).on('hashchange', readFileFromHash );

  // Call function from gallery menu
  function loadHash( hash ) {
    // Force a reload when hash did not change
    if( hash == window.location.hash ) {
      readFileFromHash();
    } else { // Hash will change: will trigger a reload
      window.location = hash;
    }
  }

  // When user selects script from gallery: load the hash
  $(".box-item").on("click", function() {
    loadHash( $(this).attr('href') );
    $("#galleryModal").toggle(); // Close the gallery
  });

  // Get the line number from a text string
  function getLineNumber( str, line ) {
    let i = str.indexOf(line);
    return (i<0) ? -1 : str.substring(0, i).split('\n').length-1;
  }

  // Load the script
  function loadScript( url = "gallery/sine.py" ) {
    // Get the file using jQuery get method
    $.get(url, function( code ) { 
      myCodeMirror.setValue( code );
      
      // Mark the required lines and make them readOnly
      requiredLines.forEach(line => {
        lineNumber = getLineNumber( code, line );
        if( lineNumber >= 0 ) {
          let start = {line: lineNumber , ch: 0};
          let end = {line:lineNumber+1, ch:0};
          myCodeMirror.markText(start, end, markOptions);
        }
      });  
    });
  }

  // Load the demo script
  readFileFromHash();

  // Event listener for uploading files
  $("#fileinput").change(function() {
    let files = this.files;
    // Use createObjectURL, this should address any CORS issues.
    let filePath = URL.createObjectURL(files[0]);
    loadScript(filePath);

    // Reset the file input such that it always triggers next change
    this.value = '';
  });

  let fileHandle;
  
  // When user click on Download script
  document.getElementById("download").onclick = async () => {
    let fileName = "charts.py";
    let hashFile = window.location.hash.substr(1);
    if( fileHandle ) fileName = fileHandle.name;
    else if( hashFile != "" ) fileName = hashFile;
    
    if( window.showSaveFilePicker ) {
      fileHandle = await window.showSaveFilePicker({
        suggestedName: fileName,
        startIn: fileHandle || "downloads",
        types: [{
          description: 'Python script',
          accept: {
            'text/plain': ['.py'],
          },
        }],
      });
     await writeFile( fileHandle, myCodeMirror.getValue() );
    $("#save").removeAttr('disabled');      
    } else { // legacy method
      var newFilename = prompt("Download as...", fileName);
      if (newFilename != null && newFilename != "") {
        let url = 'data:text/plain;charset=utf-8,' + encodeURIComponent( myCodeMirror.getValue() ) ;
        downloadURL( url, newFilename );
      }
    }
  }

  // When user click on save button
  document.getElementById("save").onclick = async () => {
    await writeFile( fileHandle, myCodeMirror.getValue() );    
  }

  async function writeFile(fileHandle, contents) {
    // Support for Chrome 82 and earlier.
    if (fileHandle.createWriter) {
      // Create a writer (request permission if necessary).
      const writer = await fileHandle.createWriter();
      // Write the full length of the contents
      await writer.write(0, contents);
      // Close the file and write the contents to disk
      await writer.close();
      return;
    }
    // For Chrome 83 and later.
    // Create a FileSystemWritableFileStream to write to.
    const writable = await fileHandle.createWritable();
    // Write the contents of the file to the stream.
    await writable.write(contents);
    // Close the file and write the contents to disk.
    await writable.close();
  }
  
  // Make a downloadable element
  function downloadURL( url, newFileName ) {
    var link = document.createElement("a");
    document.body.appendChild(link); // for Firefox
    link.setAttribute("href", url);
    link.setAttribute("download", newFileName );
    link.click();
    document.body.removeChild(link);
  }
  
  // Initialize Pyodide
  let pyodide;
  const output = document.getElementById("output");
  output.value = 'Initializing... Please wait... \n';
  async function main(){
    pyodide = await loadPyodide();
    await pyodide.loadPackage("matplotlib");
    await pyodide.runPythonAsync( startupCode );
    output.value += 'Ready!\n';
    $("#runCode").removeAttr('disabled');
  }
  let pyodideReadyPromise = main();

  // Evaluate the python user code
  async function evaluatePython() {
    output.value = "Processing script...\n";
    await pyodideReadyPromise;
    try {
      let pythonOutput = await pyodide.runPythonAsync( myCodeMirror.getValue() );
      output.value += "Done!\n";
      addToOutput( pythonOutput );
      showFigure();
    } catch(err) {
      addToOutput(err);
    }
  }

  // Print the output from the Python user code
  function addToOutput(s) {
    // Print stdout
    var stdout = pyodide.runPython("sys.stdout.getvalue()")
    pyodide.runPython("sys.stdout = io.StringIO()"); // clear previous stdout
    output.value += stdout;
    
    // Print output value (unless it is undefined)
    if( s ) output.value += s + '\n';

    // Move to last line
    output.scrollTop = output.scrollHeight;
  }

  // Draw the matplotlib figure in the HTML DOM
  let lastID;
  function showFigure() {
    // Remove the previous div first
    if( lastID ) {
      document.getElementById(lastID).remove();
    }

    // Use the built-in show() method
    pyodide.runPython("f = plt.gcf()");
    pyodide.runPython("f.canvas.create_root_element = create_root_element1.__get__(f.canvas, f.canvas.__class__)");
    pyodide.runPython("f.canvas.show()");
    pyodide.runPython("lastID = f.canvas._id");

    // Store the id of the output canvas
    lastID = pyodide.globals.get('lastID')
  }


  /* ============= MODAL SECTION =================
     Define functions for the modal boxes.
     Shows and hides the modal boxes.
     =========================================== */    

  // Event listener for the different modal boxes
  $("#gallery").click( evt => { showModal("galleryModal"); });
  $("#showHelp").click( evt => { showModal("helpModal");} );
  
  // Showing modal box
  function showModal(name) { $("#"+name).toggle(); }

  // When the user clicks on <span> (x), close the current modal
  $(".close").on("click", function() { $(this).parent().parent().toggle(); });
  
  // When the user clicks anywhere outside of the modal, close it
  $(window).on("click", function(event) {
    if( event.target.className === "modal" ) event.target.style.display = "none";
  });

  // set the feedback tag
  function setFeedback() {
    var name = "smackjvantilburgsmack"; // add salt
    name = name.substr(5,11); // remove salt
    $("feedback").html(name+"@gmail.com");
  }

  // load all code after the document
  $("document").ready(function(){
    // Set the feedback tag
    setFeedback();
  });
          
})();
