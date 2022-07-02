const mongoose = require('mongoose')

//Create Captains Schema

const AnalyticsSchema = new mongoose.Schema({

    testID : {
        type:String,
        required:true,
        minlength:0,
        maxlength:50
    },
    
testcenter:{
    type:String,
    required:true,
    minlength:3,
    maxlength:50

},


detected:{
   type:String,
    required:true,
    minlength:3,
    maxlength:50,

},

 gender:{
    type:String,
    required:true,
    minlength:3,
    maxlength:50,
 },

 authorized:{
    type:String,
    required:true,
    minlength:3,
    maxlength:50,
 },


});

module.exports = new mongoose.model('Analytics',AnalyticsSchema);