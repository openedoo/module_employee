'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function () {
  return gulp.src('./static/sass/**/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(gulp.dest('./static/css'));
});

gulp.task('watch', function () {
  gulp.watch('./static/sass/**/*.scss', ['sass']);
});

gulp.task('default', ['sass', 'watch']);
