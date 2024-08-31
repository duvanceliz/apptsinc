
import { CreateProjectForm } from "../components/CreateProjectForm"

export function CreateProject() {
  return (
    <div className="container">

        <div className="row">
            <div className="col-md-4"></div>
            <div className="col-md-4">
                <CreateProjectForm/>
            </div>
            <div className="col-md-4"></div>
        </div>
        
    </div>
  )
}

