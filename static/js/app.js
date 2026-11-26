const API = "/api/tareas";
const H = { "Content-Type": "application/json" };
const $ = (s) => document.querySelector(s);
const form = $("#form"), lista = $("#lista"), msg = $("#msg");
let editId = null;

function aviso(texto, ok = true) {
  msg.textContent = texto;
  msg.className = ok ? "ok" : "error";
}

function limpiar() {
  editId = null;
  form.reset();
  $("#titulo-form").textContent = "Nueva tarea";
  $("#guardar").textContent = "Guardar tarea";
  $("#cancelar").hidden = true;
}

function boton(texto, clase, accion) {
  const b = document.createElement("button");
  b.textContent = texto;
  b.className = clase;
  b.type = "button";
  b.onclick = accion;
  return b;
}

async function cargar() {
  const tareas = await (await fetch(API)).json();
  lista.replaceChildren();
  if (!tareas.length) {
    lista.textContent = "Aún no hay tareas. Registra la primera.";
    return;
  }
  tareas.forEach((t) => {
    const li = document.createElement("li");
    li.className = "tarea " + t.prioridad.toLowerCase() + (t.estado === "Terminada" ? " terminada" : "");
    const nombre = document.createElement("strong");
    nombre.textContent = t.nombre;
    const desc = document.createElement("p");
    desc.textContent = t.descripcion || "Sin descripción";
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = "Prioridad " + t.prioridad;
    const sel = document.createElement("select");
    ["Pendiente", "En proceso", "Terminada"].forEach((e) => sel.add(new Option(e, e, false, e === t.estado)));
    sel.onchange = async () => {
      await fetch(`${API}/${t.id}/estado`, { method: "PATCH", headers: H, body: JSON.stringify({ estado: sel.value }) });
      aviso("Estado actualizado.");
      cargar();
    };
    const editar = boton("Editar", "sec", () => {
      editId = t.id;
      $("#nombre").value = t.nombre;
      $("#descripcion").value = t.descripcion;
      $("#prioridad").value = t.prioridad;
      $("#estado").value = t.estado;
      $("#titulo-form").textContent = "Editar tarea";
      $("#guardar").textContent = "Guardar cambios";
      $("#cancelar").hidden = false;
      $("#nombre").focus();
    });
    const borrar = boton("Eliminar", "peligro", async () => {
      if (!confirm("¿Eliminar la tarea?")) return;
      await fetch(`${API}/${t.id}`, { method: "DELETE" });
      aviso("Tarea eliminada.");
      cargar();
    });
    const acciones = document.createElement("div");
    acciones.className = "acciones";
    acciones.append(sel, editar, borrar);
    const info = document.createElement("div");
    info.append(nombre, desc, badge);
    li.append(info, acciones);
    lista.append(li);
  });
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const cuerpo = {
    nombre: $("#nombre").value,
    descripcion: $("#descripcion").value,
    prioridad: $("#prioridad").value,
    estado: $("#estado").value,
  };
  const r = await fetch(editId ? `${API}/${editId}` : API, {
    method: editId ? "PUT" : "POST",
    headers: H,
    body: JSON.stringify(cuerpo),
  });
  const datos = await r.json();
  if (!r.ok) return aviso(datos.error, false);
  aviso(editId ? "Tarea actualizada." : "Tarea guardada correctamente.");
  limpiar();
  cargar();
};
$("#cancelar").onclick = () => { limpiar(); aviso(""); };
cargar();
