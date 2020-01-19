function initial() {

    var li, ul;

    ul = document.getElementById("myUL");

    li = ul.getElementsByTagName("li");

    for (i = 0; i < li.length; i++) {

        li[i].style.display = "none";

    }

}



initial();



function active() {

    var input, filter, ul, li, a, i, txtValue;

    input = document.getElementById("myInput");

    filter = input.value.toUpperCase();

    ul = document.getElementById("myUL");

    li = ul.getElementsByTagName("li");

    for (i = 0; i < li.length; i++) {

        a = li[i].getElementsByTagName("a")[0];

        txtValue = a.textContent || a.innerText;

        if (txtValue.toUpperCase().indexOf(filter) > -1 && filter!="" && filter.length >= 2) {

            li[i].style.display = "";

        } else {

            li[i].style.display = "none";

        }

    }

}





function draw() {

    var viz;

    var config = {

        container_id: "viz",

        server_url: "bolt://localhost:7687",

        server_user: "neo4j",

        server_password: "hackdavis2020",

        labels: {

            "ASIANSTUDIESJAPANClass": {

                "caption": "name",

                "about": "about"

            }

        },

        relationships: {

            "INTERACTS": {

                "thickness": "0.5",

                "caption": false

            }

        },

        initial_cypher: "MATCH p=(:ASIANSTUDIESJAPANClass)-[r:INTERACTS]->(:ASIANSTUDIESJAPANClass) RETURN p",

        arrows: true,

    };



    viz = new NeoVis.default(config);

    viz.render();

}
