$(function () {
    Draw();
    window.addEventListener('resize', handleResize, false);
});

// global variables
var renderer;
var scene;
var camera;
var control;
var controls;
var stats;

var offset = 40;
var offscreen = new THREE.Vector3(1000, 0, 1000);
var currentElements = [];
var newlyAddedElements = [];
var toBeRemovedElements = [];
var positionAndRotation = [];

function Draw() {
  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);

  renderer = new THREE.CSS3DRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.domElement.style.position = 'absolute';
  renderer.domElement.style.top = 0;

  camera.position.x = 750;
  camera.position.y = -45.0;
  camera.position.z = -1000;
  camera.lookAt(scene.position);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.autoRotate = true;

  $('#wrapper').append(renderer.domElement);
  updateStructure(new THREE.CylinderGeometry(40, 40, 50, 40, 9, true), 100);

  render();
};
function createCSS3DObject(iFace) {
    var div = document.createElement('div');
    var img = document.createElement('img');

    img.src = './ML/datas/faces/face_' + iFace + ".jpg";
    img.width = 340;
    img.height = 340;

    div.appendChild(img);
    div.style.opacity = 0.8;

    var object = new THREE.CSS3DObject(div);
    object.name = 'test';

    return object;
}

function updateStructure(geometry, offset) {
    positionAndRotation = getPositionAndRotation(geometry, offset);

    var tweenIn = new TWEEN.Tween({opacity: 0})
            .to({pos: 1.0}, 3000)
            .easing(TWEEN.Easing.Sinusoidal.InOut)
            .onUpdate(function () {
                var toSet = this.pos;
                newlyAddedElements.forEach(function (cssObject) {
                    cssObject.element.style.opacity = toSet;
                });

                var i = 0;
                currentElements.forEach(function (cssObject) {
                    var currentPos = positionAndRotation[i].currentPos;
                    var targetPos = positionAndRotation[i].pos;

                    var currentRotation = positionAndRotation[i].currentRotation;
                    var targetRotation = new THREE.Euler();
                    targetRotation.setFromRotationMatrix(positionAndRotation[i].rot);

                    if (currentPos) {
                        cssObject.position.x = currentPos.x + (targetPos.x - currentPos.x) * toSet;
                        cssObject.position.y = currentPos.y + (targetPos.y - currentPos.y) * toSet;
                        cssObject.position.z = currentPos.z + (targetPos.z - currentPos.z) * toSet;

                        cssObject.rotation.x = currentRotation.x + (targetRotation.x - currentRotation.x) * toSet;
                        cssObject.rotation.y = currentRotation.y + (targetRotation.y - currentRotation.y) * toSet;
                        cssObject.rotation.z = currentRotation.z + (targetRotation.z - currentRotation.z) * toSet;
                    }
                    i++;
                });
            });

    tweenIn.start();

    newlyAddedElements = [];
    toBeRemovedElements = [];

    for (var i = 0; i < positionAndRotation.length; i++) {

        if (currentElements.length > i) {
            var element = currentElements[i];
            positionAndRotation[i].currentPos = element.position.clone();
            positionAndRotation[i].currentRotation = element.rotation.clone();
        } else {
            var element = createCSS3DObject(i + 1);

            element.position = offscreen.clone();

            positionAndRotation[i].currentPos = element.position.clone();
            positionAndRotation[i].currentRotation = element.rotation.clone();

            element.element.style.opacity = 0;
            currentElements.push(element);
            newlyAddedElements.push(element);
            scene.add(element);
        }
    }
    for (var i = positionAndRotation.length; i < currentElements.length; i++) {
        toBeRemovedElements.push(currentElements[i]);
    }

    for (var i = 0; i < toBeRemovedElements.length; i++) {
        scene.remove(currentElements.pop());
    }
}

function getPositionAndRotation(geometry, offset) {
    var result = [];

    for (var iFace = 0; iFace < geometry.faces.length; iFace += 2) {
        var newPosition = new THREE.Vector3(0, 0, 0);

        var face = geometry.faces[iFace];
        var faceNext = geometry.faces[iFace + 1];
        var centroid = new THREE.Vector3();
        centroid.copy( geometry.vertices[face.a] )
                .add( geometry.vertices[face.b] )
                .add( geometry.vertices[face.c] )
                .add( geometry.vertices[faceNext.a] )
                .add( geometry.vertices[faceNext.b] )
                .add( geometry.vertices[faceNext.c] )
                .divideScalar( 6 ).multiplyScalar(offset);

        newPosition = centroid.clone();

        var up = new THREE.Vector3(0, 0, 1);
        var normal = new THREE.Vector3();
        normal.addVectors(face.normal, faceNext.normal);
        normal.divideScalar(2);

        var axis = new THREE.Vector3();
        axis.crossVectors(up, normal);

        var angle = Math.atan2(axis.length(), up.dot(normal));
        axis.normalize();

        var rotationToApply = new THREE.Matrix4();
        rotationToApply.makeRotationAxis(axis, angle);

        result.push({pos: newPosition, rot: rotationToApply});
    }

    return result;
}

function getCenter(object, face) {

    console.log(face);
    var a = object.vertices[face.a];
    var b = object.vertices[face.b];
    var c = object.vertices[face.c];

    var added = new THREE.Vector3();
    added.add(a);
    added.add(b);
    added.add(c);
    console.log(added);
    return added;
}

function render() {
    TWEEN.update();
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}

function handleResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
