import UploadBase from "@girder/components/src/utils/UploadBase";

export default class extends UploadBase {
  constructor(file, { $rest, parent } = {}) {
    super(file, {
      $rest,
      parent
    });
  }

  async start() {
    var formData = new FormData();

    var text = await new Promise(resolve => {
      var reader = new FileReader();

      reader.onload = () => {
        var text = reader.result;
        resolve(text);
      };

      reader.readAsText(this.file);
    });

    await this.$rest.post(`soil/${this.parent._id}`, { text });
  }
}
