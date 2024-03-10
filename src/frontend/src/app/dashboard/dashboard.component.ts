import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http"; 
import { throwError } from "rxjs";
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  username: string;
  history: Array<string>;
  status: "initial" | "uploading" | "success" | "fail" = "initial"; // Variable to store file status
  progress: number = 0;
  file: File | null = null; // Variable to store file

  constructor(private httpClient: HttpClient, private router: Router) { }
  ngOnInit() {
    const apiUrl = 'http://app.default.svc.cluster.local:5000/dashboard';
    // Send a POST request to the server
    const upload$ = this.httpClient.post(apiUrl, {});
    upload$.subscribe({  
      next: (data : any)=> {
        if (Object.keys(data).length === 0) {
          this.router.navigate(['/homepage']);
        } else {
          this.username = data.userdata.username;
          this.history = data.userdata.history;
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }

  // On file Select
  onUpload(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.file = file;
      const formData = new FormData();

      formData.append('file', this.file, this.file.name);

      const upload$ = this.httpClient.post("https://httpbin.org/post", formData);

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
