async function uploadFile() {
  const fileInput = document.getElementById('file-upload');
  if (!fileInput.files.length) return alert("Please select a file to upload.");

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  const response = await fetch('/upload', {
    method: 'POST',
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    populateDropdown('x-col', data.columns);
    populateDropdown('y-col', data.numeric_columns);
    populateDropdown('category-col', data.columns);
    document.getElementById('controls').style.display = 'block';
  } else {
    alert("File upload failed.");
  }
}

function populateDropdown(id, items) {
  const select = document.getElementById(id);
  select.innerHTML = '';
  const defaultOption = document.createElement('option');
  defaultOption.text = '-- Select --';
  defaultOption.disabled = true;
  defaultOption.selected = true;
  select.appendChild(defaultOption);

  items.forEach(item => {
    const option = document.createElement('option');
    option.value = item;
    option.text = item;
    select.appendChild(option);
  });
}

async function generatePlot() {
  const x = document.getElementById('x-col').value;
  const y = document.getElementById('y-col').value;
  const chart = document.getElementById('chart-type').value;
  const format = document.getElementById('format').value;
  const category = document.getElementById('category-col')?.value || null;

  const response = await fetch('/generate_plot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ x, y, chart, format, category })
  });

  if (response.ok) {
    const blob = await response.blob();
    const imgUrl = URL.createObjectURL(blob);
    const img = document.getElementById('plot-img');
    const link = document.getElementById('download-link');

    img.src = imgUrl;
    img.style.display = 'block';

    link.href = imgUrl;
    link.download = `plot.${format}`;
    link.style.display = 'block';
  } else {
    alert("Plot generation failed.");
  }
}
