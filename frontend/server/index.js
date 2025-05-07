const express = require('express');
const app = express();
const path = require('path');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const PORT = process.env.PORT || 8080;
// const router = require('./apiRoutes');
// const { db } = require('./db');

const init = async () => {
	try {
		// await db.sync();
		const server = app.listen(PORT, () =>
			console.log(`Listening to port ${PORT}`)
		);
		//MIDDLEWARE:
		app.use(morgan('dev')); // logging middleware for server logs
		app.use(express.static(path.join(__dirname, '../public'))); // static file-serving middleware
		app.use(bodyParser.json({ limit: '50mb' })); //body parsing middleware. Requests frequently contain a body - if you want to use it in req.body, then you'll need some middleware to parse the body.
		app.use(bodyParser.urlencoded({ extended: true }));

		// app.use(express.json());
		// app.use(express.urlencoded({ extended: true }));

		// app.use('/api', router); //mounting all api routes on /api - other routes collected from index.js in apiRoutes

		//Index HTML dispatch:
		//sends index.html for any requests that don't match one of our API routes.
		app.get('*', function (req, res) {
			res.sendFile(path.join(__dirname, '../public/index.html'));
		});

		//ERROR HANDLER:
		//handling 500 errors
		app.use(function (err, req, res, next) {
			console.error(err);
			console.error(err.stack);
			res
				.status(err.status || 500)
				.send(err.message || 'Error! Error! Error! ');
		});
	} catch (ex) {
		console.log(ex);
	}
};
init();
