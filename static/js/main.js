// GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById("searchForm");

let pageLinks = document.getElementsByClassName("page-link");

// ENSURE SEARCH FORM EXISTS
if (searchForm) {
  let i = 0;
  while (pageLinks.length > i) {
    pageLinks[i].addEventListener("click", function (e) {
      e.preventDefault();
      let page = this.dataset.page;
      // add hidden search input
      let tag = `<input value=${page} name="page" hidden/>`;

      searchForm.innerHTML += tag;
      searchForm.submit();
      //submit form
    });
    i++;
  }
}
