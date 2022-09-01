const windowSize = window.matchMedia("(min-width: 574px)");

function profileBar()
{
  const menuProfile = document.getElementById("profilebar");
  if(windowSize.matches)
  {
    if(menuProfile.style.left == "90%")
    {
      menuProfile.style.left = "100%";
    }
    else
    {
      menuProfile.style.left = "90%"
    }
  }
  else
  {
    if(menuProfile.style.left == "65.5%")
    {
      menuProfile.style.left = "100%";
    }
    else
    {
      menuProfile.style.left = "65.5%"
    }
  }
}

// Admin Panel

function showService()
{
    document.getElementById("tableServiceList").style.display = "none"
    document.getElementById("tablePackageList").style.display = "none"
    document.getElementById("serviceList").style.display = "none"
    document.getElementById("packageList").style.display = "none"
    document.getElementById("packageedit").style.display = "none"
    document.getElementById("serviceedit").style.display = "block"
}

function showPackage()
{
    document.getElementById("tableServiceList").style.display = "none"
    document.getElementById("tablePackageList").style.display = "none"
    document.getElementById("serviceList").style.display = "none"
    document.getElementById("packageList").style.display = "none"
    document.getElementById("serviceedit").style.display = "none"
    document.getElementById("packageedit").style.display = "block"
}

function closeService()
{
    document.getElementById("serviceedit").style.display = "none"
}

function closePackage()
{
    document.getElementById("packageedit").style.display = "none"
}

function closePackageList()
{
    document.getElementById("packageList").style.display = "none"
    document.getElementById("tablePackageList").style.display = "none"
}

function closeServiceList()
{
    document.getElementById("serviceList").style.display = "none"
    document.getElementById("tableServiceList").style.display = "none"
}

function showPackageList()
{
    document.getElementById("tableServiceList").style.display = "none"
    document.getElementById("tablePackageList").style.display = "block"
    document.getElementById("serviceedit").style.display = "none"
    document.getElementById("packageedit").style.display = "none"
    document.getElementById("serviceList").style.display = "none"
    document.getElementById("packageList").style.display = "block"
}

function showServiceList()
{
    document.getElementById("tableServiceList").style.display = "block"
    document.getElementById("tablePackageList").style.display = "none"
    document.getElementById("serviceedit").style.display = "none"
    document.getElementById("packageedit").style.display = "none"
    document.getElementById("serviceList").style.display = "block"
    document.getElementById("packageList").style.display = "none"
}

// Package Update

function sameName()
{

      if (package_name.style.display == "none")
      {
        package_name.style.display = "block"
      }
      else
      {
        package_name.style.display = "none"
      }
}
function samePrice()
{
      if (package_price.style.display == "none")
      {
        package_price.style.display = "block"
      }
      else
      {
        package_price.style.display = "none"
      }
}
function sameDescription()
{
      if (package_description.style.display == "none")
      {
        package_description.style.display = "block"
      }
      else
      {
        package_description.style.display = "none"
      }
}
function sameImage()
{
      if (package_image.style.display == "none")
      {
        package_image.style.display = "block"
      }
      else
      {
        package_image.style.display = "none"
      }
}
