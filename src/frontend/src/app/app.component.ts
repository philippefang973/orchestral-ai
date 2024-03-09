import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpEventType } from "@angular/common/http"; 
import { throwError } from "rxjs";

@Component({
  selector: 'app-root', 
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  status: "initial" | "uploading" | "success" | "fail" = "initial"; // Variable to store file status

  progress: number = 0;
  file: File | null = null; // Variable to store file

  constructor(private http: HttpClient) {}

  ngOnInit(): void {}

  // On file Select
  onChange(event: any) {
    const file: File = event.target.files[0];

    if (file) {
      this.status = "initial";
      this.file = file;
    }
  }

  onUpload() {
    if (this.file) {
      const formData = new FormData();

      formData.append('file', this.file, this.file.name);

      const upload$ = this.http.post("https://httpbin.org/post", formData);

      this.status = 'uploading';

      upload$.subscribe({  
        next: () => {
          this.status = 'success';
        },
        error: (error: any) => {
          this.status = 'fail';
          return throwError(() => error);
        },
      });
    }
  }
}