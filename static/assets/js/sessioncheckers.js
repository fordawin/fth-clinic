console.log(document.cookie.includes('type'))
if (document.cookie.includes('type')) {
    window.location.href = '/logged';
  }