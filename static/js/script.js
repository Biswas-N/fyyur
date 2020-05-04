window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

function venueDelete(venue_id) {
  fetch("/venues/" + venue_id, {
    method: "DELETE",
  })
    .then((_) => {
      window.location.replace("/venues");
    })
    .catch((err) => {
      console.log(err);
    });
}

function artistDelete(artist_id) {
  fetch("/artists/" + artist_id, {
    method: "DELETE",
  })
    .then((_) => {
      window.location.replace("/artists");
    })
    .catch((err) => {
      console.log(err);
    });
}
