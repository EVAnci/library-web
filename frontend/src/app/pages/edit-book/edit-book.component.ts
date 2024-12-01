import { Component } from '@angular/core';
import { ContextbarComponent } from '../../components/contextbar/contextbar.component';
import { NewAuthorComponent } from '../../components/new-author/new-author.component';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { BookService } from '../../services/book.service';
import { ActivatedRoute } from '@angular/router';
import { AuthorsService } from '../../services/authors.service';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-edit-book',
  standalone: true,
  imports: [ContextbarComponent, NavbarComponent, NewAuthorComponent, ReactiveFormsModule],
  templateUrl: './edit-book.component.html',
  styles: ``
})

export class EditBookComponent {
  bookId: number | null = null; // Number or null
  title: string = '';
  image: string = '';
  gender: string = '';
  book_authors: any = [];
  authors: any[] = [];
  description: string = '';
  new_authors: any[] = [];

  // Reactive Forms
  editBookForm = new FormGroup({
    titleInput: new FormControl(''),
    descriptionInput: new FormControl(''),
    authorFilter: new FormControl(''),
    genderInput: new FormControl(''),
  })

  constructor(
    private route: ActivatedRoute, 
    private bookService: BookService,
    private authorsService: AuthorsService
  ) {}

  ngOnInit() {
    this.bookId = Number(this.route.snapshot.paramMap.get('id'));
    this.getBook(this.bookId);
  }

  parseAuthors(authors: any): string[] {
    let result: string[] = [];
    for (let i = 0; i < authors.length; i++) {
      result.push(authors[i].name + ' ' + authors[i].lastname);
    }
    return result;
  }

  getAuthors() {
    const query = this.editBookForm.controls['authorFilter'].value
    if (typeof query === 'string') {
      this.authorsService.getAuthors_by_name_or_lastname(query).subscribe((answer:any) => {
        this.authors = answer.authors;
      })
    } else {
      this.authorsService.getAuthors_by_name_or_lastname('').subscribe((answer:any) => {
        this.authors = answer.authors;
      })
    }
  }

  repeatedAuthor(test_id: number): boolean {
    for (let id of this.new_authors) {
      if (id == test_id) {
        return true
      }
    }
    return false
  }

  addAuthor() {
    const input = this.editBookForm.controls['authorFilter'].value;
    const name: string = input?.split(' ')[0] || '';
    const lastname: string = input?.split(' ')[1] || '';
    if (!name || !lastname) {
      return;
    } else {
      this.authorsService.getAuthor_by_fullname(name, lastname).subscribe((answer:any) => {
        const id = answer.authors[0].id;
        if (id && !(this.repeatedAuthor(id))) {
          this.new_authors.push(id);
          this.book_authors.push(answer.authors[0]);
          this.editBookForm.controls['authorFilter'].setValue('');
        }
      })      
    }
  }

  deleteAuthor(id: number) {
    for (let i = 0; i < this.new_authors.length; i++) {
      if (this.new_authors[i] == id) {
        this.new_authors.splice(i, 1);
      }
    }
    for (let i = 0; i < this.book_authors.length; i++) {
      if (this.book_authors[i].id == id) {
        this.book_authors.splice(i, 1);
      }
    }
  }

  getBook(id: Number) {
    this.bookService.getBook(id).subscribe((answer:any) => {
      this.title = answer.title
      this.image = answer.image
      this.gender = answer.gender
      this.description = answer.description
      if (answer.authors.length > 0) {
        this.book_authors = answer.authors
        for (let author of answer.authors) {
          this.new_authors.push(author.id);
        }
      }
    })
  }

  uploadImage(event: any) {
    console.log(event);
  }

  save() {
    console.log(this.editBookForm.value);
  }
}
