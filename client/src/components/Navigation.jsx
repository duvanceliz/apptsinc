
export function Navigation() {
  return (
    <nav className="navbar navbar-expand-lg navbar navbar-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#" >T&S INC</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-end" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <a className="nav-link active fs-5" aria-current="page" href="">Inicio</a>
              
             
              <a className="nav-link disabled" href="#" tabIndex="-1" aria-disabled="true">Ofertas</a>
            </div>
          </div>
        </div>
      </nav>
  )
}

