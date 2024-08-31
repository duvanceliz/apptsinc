import { TrTable } from "./TrTable";

export function Table({ projects, triggerReloadOffers }) {
  return (
    <div>
        
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">NOMBRE</th>
            <th scope="col">EMPRESA</th>
            <th scope="col">NIT</th>
            <th scope="col">Asesor</th>
            <th scope="col">Estado</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <TrTable key={project.id} project={project} triggerReloadOffers = {triggerReloadOffers} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
