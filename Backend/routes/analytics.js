const express = require('express');

const router = express.Router();
const Analytics = require('../models/analytics')


router.post('/',(req,res)=>{


    analytic = new Analytics({
        testID : req.body.testID,
        testcenter : req.body.testcenter,
        detected:req.body.detected,
        gender:req.body.gender,
        authorized:req.body.authorized,

   
    })

    analytic.save().then(analytic =>{
      //  console.log(res)
        res.send(analytic);
    }).catch(error=>{
        console.log(error)
        res.status(500).send(error)
    });
});

//GET ALL CAPTAINS
router.get('/',(req,res)=>{

    Analytics.find()
    .then((analytic)=>res.send({analytics: analytic}))
    .catch((error)=>{
        res.status(500).send("Cannot Get");
    });
})

// //GET CAPTAIN BY ID
// router.get("/:capId",(req, res)=>{

//     Captain.findById(req.params.capId).then(captain=>{
//         if(captain) res.send({captains: captain});
//         res.status(404).json.send("Captain Not Found")
//     })
//     .catch((error)=>{
//         res.status(500).send(error.message)
//     })


// })



module.exports = router;