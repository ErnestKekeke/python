async function updateUser(id) {
  const response = await fetch(`http://127.0.0.1:5001/posts/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'Updated Title',
      content: 'Updated content here'
    })
  });

  const data = await response.json();
  console.log(data);
}

updateUser(1);