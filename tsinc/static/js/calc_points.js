const module_points = document.getElementById("module-points");
const pd_eu = document.getElementById("pd-eu");
const pd_ed = document.getElementById("pd-ed");
const pd_sa = document.getElementById("pd-sa");
const pd_sd = document.getElementById("pd-sd");
const pd_sc = document.getElementById("pd-sc");
const pd_array = [pd_eu, pd_ed, pd_sa, pd_sd, pd_sc];
const pp_eu = document.getElementById("pp-eu");
const pp_ed = document.getElementById("pp-ed");
const pp_sa = document.getElementById("pp-sa");
const pp_sd = document.getElementById("pp-sd");
const pp_sc = document.getElementById("pp-sc");

const pp_array = [pp_eu, pp_ed, pp_sa, pp_sd, pp_sc];
const ps_eu = document.getElementById("ps-eu");
const ps_ed = document.getElementById("ps-ed");
const ps_sa = document.getElementById("ps-sa");
const ps_sd = document.getElementById("ps-sd");
const ps_sc = document.getElementById("ps-sc");
const ps_array = [ps_eu, ps_ed, ps_sa, ps_sd, ps_sc];
const total_point_item = document.getElementById("total-point-item");

const points = [];

const total_point_i = [];

for (let tr of module_points.getElementsByTagName("tr")) {
  // Itera a través de los td dentro de cada tr
  const point = [];
  for (let td of tr.getElementsByTagName("td")) {
    // Obtiene el texto dentro de cada td
    // console.log(td.textContent);
    point.push(parseInt(td.textContent));
  }
  point.pop();
  point.shift();
  points.push(point);
}

for (let tr of total_point_item.getElementsByTagName("tr")) {
  // Itera a través de los td dentro de cada tr
  const point = [];
  for (let td of tr.getElementsByTagName("td")) {
    // Obtiene el texto dentro de cada td
    // console.log(td.textContent);
    point.push(parseInt(td.textContent));
  }
  point.shift();
  total_point_i.push(point);
}

// console.log(total_point_i);

// console.log(points)

let pd = points.reduce((acc, curr) => {
  return acc.map((num, idx) => num + curr[idx]);
});

function print_p(array, p_array) {
  for (let i = 0; i < 5; i++) {
    array[i].innerText = p_array[i];
  }
}

print_p(pd_array, pd);

pp = new Array(5).fill(0);

const t_point_i = total_point_i[0];

let result = 0,
  result2 = 0,
  result3 = 0;

for (let i = 1; i < 4; i++) {
  if (t_point_i[i] === 0) {
    pp[i] = 0;
    pp[i - 1] = t_point_i[i - 1];
  } else if (pd[i] >= t_point_i[i]) {
    pp[i] = t_point_i[i];
  } else {
    pp[i] = pd[i];
    result = Math.abs(t_point_i[i] - pd[i]);
    if (i === 1) {
      pp[0] = t_point_i[0] + result;
    } else if (i === 2) {
      result2 = result;
    } else if (i === 3) {
      result3 = result + result2;
      pp[i + 1] = result3;
    }
  }
}

print_p(pp_array, pp);

ps = new Array(5).fill(0);

ps = pd.map((value, index) => value - pp[index]);

function point_bcolor(array) {
  for (let i = 0; i < 5; i++) {
    if (ps[i] >= 0) {
      array[i].style.background = "#4CAE2B";
    } else {
      array[i].style.background = "#C70039";
    }
  }
}

point_bcolor(ps_array);
print_p(ps_array, ps);
